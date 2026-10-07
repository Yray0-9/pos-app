from decimal import Decimal
from uuid import UUID

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .cart import calculate_order
from .models import Product, Transaction, TransactionItem


class CartTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', verbosity=0)
        cls.rice = Product.objects.get(seed_key='rice-bowl')
        cls.wrap = Product.objects.get(seed_key='chicken-wrap')
        cls.drink = Product.objects.get(seed_key='cucumber-lemonade')

    def act(self, action, product=None, **extra):
        data = {'action': action, **extra}
        if product is not None:
            data['product_id'] = str(product.pk)
        return self.client.post(reverse('kiosk:cart_action'), data,
                                HTTP_ACCEPT='application/json')

    def order(self):
        return calculate_order(self.client.session.get('kiosk', {}).get('cart', {}))

    def save_state(self, state):
        session = self.client.session
        session['kiosk'] = state
        session.save()

    def test_catalog_and_empty_order_cannot_advance(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['catalog']), 6)
        for product in Product.objects.all():
            self.assertContains(response, product.name)
            self.assertContains(response, f'₱{product.price:.2f}')
        self.assertContains(response, 'id="review-order" type="button" disabled')
        self.assertContains(response, 'Tap an item on the menu')
        self.assertEqual(response.context['order']['total'], Decimal('0.00'))
        self.assertNotIn('kiosk', self.client.session)

    def test_complete_selection_arithmetic_and_removal_sequence(self):
        for product in (self.rice, self.rice, self.wrap, self.drink):
            self.assertEqual(self.act('add', product).status_code, 200)
        order = self.order()
        self.assertEqual(order['item_count'], 4)
        self.assertEqual([line['subtotal'] for line in order['lines']],
                         [Decimal('170.00'), Decimal('70.00'), Decimal('39.50')])
        self.assertEqual(order['total'], Decimal('279.50'))
        self.act('increase', self.rice)
        self.assertEqual(self.order()['total'], Decimal('364.50'))
        self.act('decrease', self.rice)
        self.assertEqual(self.order()['total'], Decimal('279.50'))
        self.act('remove', self.drink)
        self.assertEqual(self.order()['total'], Decimal('240.00'))
        self.act('decrease', self.wrap)
        self.assertNotIn(str(self.wrap.pk), self.order()['cart'])
        self.act('remove', self.rice)
        self.assertEqual(self.order()['total'], Decimal('0.00'))
        self.assertEqual(self.act('decrease', self.rice).status_code, 400)
        self.assertEqual(self.order()['cart'], {})
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(TransactionItem.objects.count(), 0)

    def test_persistence_session_isolation_and_owned_state(self):
        session = self.client.session
        session['unrelated'] = {'keep': True}
        session.save()
        self.act('add', self.rice)
        original = self.client.session['kiosk']
        UUID(original['customer_context'])
        self.client.get('/')
        self.assertEqual(self.client.session['kiosk'], original)
        self.assertEqual(Client().get('/').context['order']['cart'], {})
        state = original.copy()
        state.update(reviewed_order={'stale': True}, payment_attempt='old',
                     payment_method='cash', cash_amount='100')
        self.save_state(state)
        self.act('increase', self.rice)
        updated = self.client.session['kiosk']
        self.assertEqual(updated['revision'], original['revision'] + 1)
        self.assertEqual(updated['customer_context'], original['customer_context'])
        self.assertEqual(self.client.session['unrelated'], {'keep': True})
        self.assertNotIn('reviewed_order', updated)
        self.assertNotIn('payment_attempt', updated)

    def test_browser_money_and_direct_quantities_are_never_trusted(self):
        self.act('add', self.rice, price='0.01', total='0.01', quantity='-999')
        self.assertEqual(self.order()['total'], Decimal('85.00'))
        self.assertEqual(self.order()['cart'], {str(self.rice.pk): 1})
        self.act('increase', self.rice, quantity='1.5', subtotal='0')
        self.assertEqual(self.order()['total'], Decimal('170.00'))

    def test_invalid_actions_identifiers_and_absent_items_leave_state_intact(self):
        self.act('add', self.rice)
        original = self.client.session['kiosk']
        invalid = ('', '0', '-1', '1.5', 'NaN', 'true', '01', '9' * 30,
                   '9223372036854775808', '9999999', '１')
        for identifier in invalid:
            with self.subTest(identifier=identifier):
                response = self.act('add', product_id=identifier)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.client.session['kiosk'], original)
                self.assertIn('role="alert"', response.json()['html'])
        for action in ('pay', 'set', '', 'refresh'):
            self.assertEqual(self.act(action, self.rice).status_code, 400)
            self.assertEqual(self.client.session['kiosk'], original)
        self.assertEqual(self.act('increase', self.wrap).status_code, 400)

    def test_quantity_limit_and_recovery(self):
        self.save_state({'cart': {str(self.rice.pk): 98}})
        self.act('add', self.rice)
        self.assertEqual(self.order()['cart'][str(self.rice.pk)], 99)
        original = self.client.session['kiosk']
        for action in ('add', 'increase'):
            self.assertEqual(self.act(action, self.rice).status_code, 400)
            self.assertEqual(self.client.session['kiosk'], original)
        self.act('decrease', self.rice)
        self.assertEqual(self.order()['cart'][str(self.rice.pk)], 98)

    def test_corrupt_quantities_read_only_warning_and_explicit_repair(self):
        for bad in (-1, 0, 100, 1.5, True, '2', None):
            with self.subTest(quantity=bad):
                raw = {str(self.rice.pk): bad, str(self.wrap.pk): 2, '-1': 1}
                self.save_state({'cart': raw})
                response = self.client.get('/')
                self.assertTrue(response.context['order']['needs_refresh'])
                self.assertEqual(response.context['order']['total'], Decimal('140.00'))
                self.assertEqual(self.client.session['kiosk']['cart'], raw)
                self.assertEqual(self.act('refresh').status_code, 200)
                self.assertEqual(self.order()['cart'], {str(self.wrap.pk): 2})
        for damaged in (None, 'broken', []):
            self.save_state({'cart': damaged})
            self.assertTrue(self.client.get('/').context['order']['needs_refresh'])
            self.act('refresh')
            self.assertEqual(self.order()['cart'], {})
        self.save_state('broken namespace')
        self.assertTrue(self.client.get('/').context['order']['needs_refresh'])
        self.act('refresh')
        self.assertEqual(self.order()['cart'], {})

    def test_current_catalog_prices_and_unavailable_items(self):
        self.act('add', self.rice)
        self.act('add', self.drink)
        Product.objects.filter(pk=self.rice.pk).update(price=Decimal('85.50'))
        self.assertEqual(self.client.get('/').context['order']['total'], Decimal('125.00'))
        Product.objects.filter(pk=self.drink.pk).update(is_available=False)
        response = self.client.get('/')
        self.assertTrue(response.context['order']['needs_refresh'])
        self.assertEqual(response.context['order']['total'], Decimal('85.50'))
        self.assertIn(str(self.drink.pk), self.client.session['kiosk']['cart'])
        self.assertEqual(self.act('add', self.drink).status_code, 400)
        self.act('refresh')
        self.assertNotIn(str(self.drink.pk), self.order()['cart'])
        self.rice.delete()
        self.assertTrue(self.client.get('/').context['order']['needs_refresh'])
        self.act('refresh')
        self.assertEqual(self.order()['total'], Decimal('0.00'))

    def test_total_storage_limit_blocks_growth_but_allows_reduction(self):
        Product.objects.filter(pk__in=(self.rice.pk, self.wrap.pk)).update(
            price=Decimal('999999.99'))
        self.save_state({'cart': {str(self.rice.pk): 99}})
        self.act('add', self.wrap)
        self.assertEqual(self.order()['total'], Decimal('99999999.00'))
        original = self.client.session['kiosk']
        self.assertEqual(self.act('increase', self.wrap).status_code, 400)
        self.assertEqual(self.client.session['kiosk'], original)
        self.save_state({'cart': {str(self.rice.pk): 99, str(self.wrap.pk): 99}})
        self.assertTrue(self.client.get('/').context['order']['over_limit'])
        self.assertEqual(self.act('decrease', self.wrap).status_code, 200)
        self.assertEqual(self.act('remove', self.wrap).status_code, 200)
        self.assertFalse(self.order()['over_limit'])

    def test_post_csrf_native_fallback_and_escaped_feedback(self):
        self.assertEqual(self.client.get(reverse('kiosk:cart_action')).status_code, 405)
        self.assertEqual(self.client.post('/').status_code, 405)
        protected = Client(enforce_csrf_checks=True)
        self.assertEqual(protected.post(reverse('kiosk:cart_action'),
                                       {'action': 'add', 'product_id': self.rice.pk}).status_code, 403)
        protected.get('/')
        token = protected.cookies['csrftoken'].value
        self.rice.name = '<script>alert(1)</script>'
        self.rice.save()
        response = protected.post(reverse('kiosk:cart_action'),
                                  {'action': 'add', 'product_id': self.rice.pk,
                                   'csrfmiddlewaretoken': token}, follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, 'id="review-order" type="button" disabled')
        self.assertIn('no-store', response.headers['Cache-Control'])
        Product.objects.all().update(is_available=False)
        self.assertContains(self.client.get('/'), 'No items are available right now')
