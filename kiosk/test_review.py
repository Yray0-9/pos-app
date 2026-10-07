from decimal import Decimal
from uuid import UUID

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .models import Product, Transaction, TransactionItem


class ReviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', verbosity=0)
        cls.rice = Product.objects.get(seed_key='rice-bowl')
        cls.wrap = Product.objects.get(seed_key='chicken-wrap')
        cls.drink = Product.objects.get(seed_key='cucumber-lemonade')

    def edit(self, action, product):
        return self.client.post(reverse('kiosk:cart_action'),
                                {'action': action, 'product_id': product.pk})

    def build_order(self):
        for product in (self.rice, self.rice, self.wrap, self.drink):
            self.edit('add', product)

    def review(self):
        return self.client.get(reverse('kiosk:review'))

    def continue_order(self, token, client=None, **extra):
        return (client or self.client).post(reverse('kiosk:continue_payment'),
                                           {'review_token': token, **extra}, follow=True)

    def replace_state(self, state):
        session = self.client.session
        session['kiosk'] = state
        session.save()

    def test_summary_agrees_with_selection_and_back_does_not_mutate(self):
        self.build_order()
        state = self.client.session['kiosk']
        selected = self.client.get('/').context['order']
        response = self.review()
        self.assertEqual(response.context['order'], selected)
        for value in ('Chicken Rice Bowl', 'Chicken Wrap', 'Cucumber Lemonade',
                      '₱85.00', '₱170.00', '₱70.00', '₱39.50', '₱279.50',
                      'Back to selection', 'Continue to Payment'):
            self.assertContains(response, value)
        self.assertEqual(self.client.session['kiosk'], state)
        for _ in range(3):
            self.client.get('/')
            self.review()
            self.assertEqual(self.client.session['kiosk'], state)
        self.assertIn('no-store', response.headers['Cache-Control'])

    def test_edits_after_back_recalculate_and_invalidate_old_confirmation(self):
        self.build_order()
        old_token = self.review().context['review_token']
        self.client.get('/')
        self.edit('increase', self.rice)
        self.assertEqual(self.review().context['order']['total'], Decimal('364.50'))
        response = self.continue_order(old_token)
        self.assertEqual(response.redirect_chain, [('/review/', 302)])
        self.assertContains(response, 'Your order changed.')
        self.assertNotIn('reviewed_order', self.client.session['kiosk'])
        self.edit('decrease', self.rice)
        self.edit('remove', self.drink)
        self.assertEqual(self.review().context['order']['total'], Decimal('240.00'))
        fresh = self.review().context['review_token']
        self.assertEqual(self.continue_order(fresh).redirect_chain, [('/payment/', 302)])

    def test_confirmed_payment_entry_stable_attempt_and_no_completed_sale(self):
        self.build_order()
        token = self.review().context['review_token']
        response = self.continue_order(token, price='0.01', total='0.01')
        self.assertEqual(response.redirect_chain, [('/payment/', 302)])
        self.assertContains(response, '₱279.50')
        self.assertContains(response, 'Payment is not available yet.')
        first = self.client.session['kiosk']
        UUID(first['payment_attempt'])
        self.assertEqual(first['reviewed_order']['total'], '279.50')
        self.assertEqual(first['reviewed_order']['items'][0]['quantity'], 2)
        self.assertEqual(first['reviewed_order']['items'][0]['unit_price'], '85.00')
        for _ in range(3):
            self.client.get(reverse('kiosk:payment'))
            fresh = self.review().context['review_token']
            self.continue_order(fresh)
            self.assertEqual(self.client.session['kiosk'], first)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(TransactionItem.objects.count(), 0)

    def test_empty_cart_cannot_advance_even_with_old_or_forged_token(self):
        response = self.review()
        self.assertContains(response, 'Your order is empty.')
        self.assertContains(response, 'id="continue-payment" type="submit" disabled')
        self.assertIsNone(response.context['review_token'])
        self.assertEqual(self.continue_order('forged').redirect_chain, [('/review/', 302)])
        self.assertNotIn('kiosk', self.client.session)
        self.edit('add', self.rice)
        token = self.review().context['review_token']
        self.edit('remove', self.rice)
        self.assertContains(self.continue_order(token), 'Your order is empty.')
        self.assertNotIn('payment_attempt', self.client.session['kiosk'])

    def test_missing_unavailable_and_corrupt_items_block_until_explicit_repair(self):
        for condition in ('unavailable', 'missing', 'invalid'):
            with self.subTest(condition=condition):
                Product.objects.filter(pk=self.drink.pk).update(is_available=True)
                self.build_order()
                token = self.review().context['review_token']
                state = self.client.session['kiosk']
                if condition == 'unavailable':
                    Product.objects.filter(pk=self.drink.pk).update(is_available=False)
                elif condition == 'missing':
                    state['cart']['9999999'] = 1
                    self.replace_state(state)
                else:
                    state['cart'][str(self.drink.pk)] = -1
                    self.replace_state(state)
                raw = self.client.session['kiosk']
                response = self.review()
                self.assertIsNone(response.context['review_token'])
                self.assertContains(response, 'Go back and update your order')
                self.assertEqual(self.client.session['kiosk'], raw)
                self.assertEqual(self.continue_order(token).redirect_chain, [('/review/', 302)])
                self.client.get('/')
                self.assertEqual(self.client.session['kiosk'], raw)
                self.client.post(reverse('kiosk:cart_action'), {'action': 'refresh'})
                self.assertIsNotNone(self.review().context['review_token'])
                self.replace_state({})

    def test_catalog_price_and_name_changes_require_review_again(self):
        self.build_order()
        original_token = self.review().context['review_token']
        self.continue_order(original_token)
        first_attempt = self.client.session['kiosk']['payment_attempt']
        Product.objects.filter(pk=self.rice.pk).update(price=Decimal('86.00'))
        response = self.client.get(reverse('kiosk:payment'), follow=True)
        self.assertEqual(response.redirect_chain, [('/review/', 302)])
        self.assertContains(response, '₱281.50')
        self.assertContains(self.continue_order(original_token), 'Your order changed.')
        price_token = self.review().context['review_token']
        Product.objects.filter(pk=self.rice.pk).update(name='Updated Rice Bowl')
        self.assertContains(self.continue_order(price_token), 'Your order changed.')
        current = self.review().context['review_token']
        self.continue_order(current)
        state = self.client.session['kiosk']
        self.assertNotEqual(state['payment_attempt'], first_attempt)
        self.assertEqual(state['reviewed_order']['total'], '281.50')
        self.assertEqual(state['reviewed_order']['items'][0]['name'], 'Updated Rice Bowl')

    def test_all_unavailable_or_deleted_items_explain_repair_before_empty_order(self):
        self.edit('add', self.rice)
        raw = self.client.session['kiosk']
        Product.objects.filter(pk=self.rice.pk).update(is_available=False)
        for deleted in (False, True):
            if deleted:
                self.rice.delete()
            response = self.review()
            self.assertTrue(response.context['order']['needs_refresh'])
            self.assertContains(response, 'Some saved items are invalid or unavailable.')
            self.assertIsNone(response.context['review_token'])
            self.assertEqual(self.client.session['kiosk'], raw)
        self.client.post('/cart/', {'action': 'refresh'})
        response = self.review()
        self.assertContains(response, 'Your order is empty.')
        self.assertFalse(response.context['order']['needs_refresh'])
        self.assertEqual(self.client.session['kiosk']['cart'], {})

    def test_tampered_missing_and_other_session_tokens_are_rejected(self):
        self.build_order()
        token = self.review().context['review_token']
        original = self.client.session['kiosk']
        for invalid in ('', 'forged', token + 'x'):
            response = self.continue_order(invalid)
            self.assertEqual(response.redirect_chain, [('/review/', 302)])
            self.assertEqual(self.client.session['kiosk'], original)
        other = Client()
        other.post(reverse('kiosk:cart_action'), {'action': 'add', 'product_id': self.rice.pk})
        rejected = self.continue_order(token, client=other)
        self.assertEqual(rejected.redirect_chain, [('/review/', 302)])
        self.assertNotIn('reviewed_order', other.session['kiosk'])

    def test_direct_payment_entry_requires_current_confirmation(self):
        self.build_order()
        self.assertEqual(self.client.get('/payment/').url, '/review/')
        token = self.review().context['review_token']
        self.continue_order(token)
        self.client.get('/')
        self.edit('decrease', self.rice)
        self.assertEqual(self.client.get('/payment/').url, '/review/')
        self.assertNotIn('payment_attempt', self.client.session['kiosk'])
        new_token = self.review().context['review_token']
        self.continue_order(new_token)
        state = self.client.session['kiosk']
        state['payment_attempt'] = 'invalid'
        self.replace_state(state)
        self.assertEqual(self.client.get('/payment/').url, '/review/')

    def test_limits_and_malformed_session_metadata_do_not_advance(self):
        self.build_order()
        original = self.client.session['kiosk']
        for field, invalid in (('customer_context', 'invalid'), ('revision', True)):
            state = original.copy()
            state[field] = invalid
            self.replace_state(state)
            self.assertIsNone(self.review().context['review_token'])
            self.assertEqual(self.continue_order('invalid').redirect_chain, [('/review/', 302)])
        state = original.copy()
        state['cart'] = {str(self.rice.pk): 99, str(self.wrap.pk): 99}
        Product.objects.filter(pk__in=(self.rice.pk, self.wrap.pk)).update(price=Decimal('999999.99'))
        self.replace_state(state)
        response = self.review()
        self.assertTrue(response.context['order']['over_limit'])
        self.assertIsNone(response.context['review_token'])
        self.assertEqual(self.continue_order('invalid').redirect_chain, [('/review/', 302)])

    def test_post_csrf_and_get_navigation_boundaries(self):
        self.assertEqual(self.client.get('/review/continue/').status_code, 405)
        self.assertEqual(self.client.post('/review/').status_code, 405)
        self.assertEqual(self.client.post('/payment/').status_code, 405)
        guarded = Client(enforce_csrf_checks=True)
        guarded.get('/')
        csrf = guarded.cookies['csrftoken'].value
        guarded.post('/cart/', {'action': 'add', 'product_id': self.rice.pk,
                                'csrfmiddlewaretoken': csrf})
        token = guarded.get('/review/').context['review_token']
        self.assertEqual(guarded.post('/review/continue/', {'review_token': token}).status_code, 403)
        self.assertNotIn('reviewed_order', guarded.session['kiosk'])
        response = guarded.post('/review/continue/', {'review_token': token,
                                'csrfmiddlewaretoken': csrf}, follow=True)
        self.assertEqual(response.redirect_chain, [('/payment/', 302)])
        self.assertIn('no-store', response.headers['Cache-Control'])
