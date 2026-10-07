from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch
from uuid import UUID

from django.core.management import call_command
from django.test import Client, TestCase, TransactionTestCase

from .cart import CartError
from .checkout import complete_payment, payment_token
from .models import Product, Transaction, TransactionItem


class CheckoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', verbosity=0)
        cls.rice = Product.objects.get(seed_key='rice-bowl')
        cls.wrap = Product.objects.get(seed_key='chicken-wrap')
        cls.drink = Product.objects.get(seed_key='cucumber-lemonade')

    def edit(self, action, product=None, client=None):
        return (client or self.client).post('/cart/', {
            'action': action, 'product_id': str(product.pk) if product else ''})

    def order(self):
        for product in (self.rice, self.rice, self.wrap, self.drink):
            self.edit('add', product)

    def review(self):
        return self.client.get('/review/')

    def confirm(self):
        token = self.review().context['review_token']
        return self.client.post('/review/continue/', {'review_token': token})

    def pay(self, method='cash', amount='300.00', token=None, follow=True):
        if token is None:
            token = self.client.get(f'/payment/{method}/').context['payment_token']
        return self.client.post(f'/payment/{method}/complete/',
                                {'payment_token': token, 'amount_paid': amount,
                                 'total': '0.01', 'price': '0.01'}, follow=follow)

    def reset(self):
        token = self.client.get('/receipt/').context['reset_token']
        return self.client.post('/new-transaction/', {'reset_token': token}, follow=True)

    def test_review_agrees_and_repeated_back_preserves_quantities(self):
        self.order()
        saved = deepcopy(self.client.session['kiosk'])
        selected = self.client.get('/').context['order']
        for _ in range(3):
            reviewed = self.review()
            self.assertEqual(reviewed.context['order'], selected)
            self.assertContains(reviewed, '₱279.50')
            self.assertContains(reviewed, 'Back to selection')
            self.client.get('/')
            self.assertEqual(self.client.session['kiosk'], saved)
        self.assertIn('no-store', reviewed.headers['Cache-Control'])

    def test_back_edits_recalculate_and_old_confirmation_is_rejected(self):
        self.order()
        old = self.review().context['review_token']
        self.client.get('/')
        self.edit('increase', self.rice)
        self.assertEqual(self.review().context['order']['total'], Decimal('364.50'))
        self.assertContains(self.client.post('/review/continue/', {'review_token': old}, follow=True),
                            'Your order changed.')
        self.edit('decrease', self.rice)
        self.edit('remove', self.drink)
        self.assertEqual(self.review().context['order']['total'], Decimal('240.00'))
        self.assertEqual(self.confirm().url, '/payment/')

    def test_empty_direct_payment_success_and_receipt_are_guarded(self):
        review = self.review()
        self.assertContains(review, 'Your order is empty.')
        self.assertIsNone(review.context['review_token'])
        for path in ('/payment/', '/payment/cash/', '/success/', '/receipt/'):
            self.assertEqual(self.client.get(path).status_code, 302)
        response = self.client.post('/payment/cash/complete/', {'amount_paid': '300'}, follow=True)
        self.assertEqual(response.redirect_chain[0], ('/review/', 302))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_three_payment_choices_and_method_instructions(self):
        self.order()
        self.confirm()
        response = self.client.get('/payment/')
        for text in ('Cash', 'QR Payment', 'Credit/Debit Card'):
            self.assertContains(response, text)
        for method, text in (('cash', 'Cash amount received'),
                             ('qr', 'DEMO PLACEHOLDER'), ('card', 'Tap, insert or swipe')):
            self.assertContains(self.client.get(f'/payment/{method}/'), text)

    def test_invalid_and_insufficient_cash_create_no_sale(self):
        self.order()
        self.confirm()
        for value in ('', '   ', 'text', 'NaN', 'Infinity', '-1', '0', '1', '279.49',
                      '1.234', '1e3', '100,000', '99999999.999', '100000000'):
            with self.subTest(cash=value):
                response = self.pay(amount=value)
                self.assertEqual(response.status_code, 400)
                self.assertTemplateUsed(response, 'kiosk/payment.html')
                self.assertNotContains(response, 'Payment successful', status_code=400)
                self.assertEqual(Transaction.objects.count(), 0)
                self.assertEqual(TransactionItem.objects.count(), 0)
                self.assertEqual(self.client.get('/receipt/').url, '/')

    def test_exact_and_excess_cash_totals_and_receipts(self):
        for paid, change in (('279.50', '0.00'), ('300.00', '20.50')):
            with self.subTest(paid=paid):
                self.order()
                self.confirm()
                response = self.pay(amount=paid)
                self.assertContains(response, 'Payment successful')
                sale = Transaction.objects.latest('id')
                self.assertEqual(sale.total, Decimal('279.50'))
                self.assertEqual(sale.amount_paid, Decimal(paid))
                self.assertEqual(sale.change, Decimal(change))
                self.assertEqual(sum(sale.items.values_list('subtotal', flat=True)), sale.total)
                receipt = self.client.get('/receipt/')
                for value in (sale.reference, 'Asia/Singapore', 'Chicken Rice Bowl',
                              'Quantity 2', '₱85.00', '₱170.00', '₱279.50', f'₱{change}'):
                    self.assertContains(receipt, value)
                self.reset()

    def test_qr_and_card_complete_exactly_with_zero_change(self):
        references = []
        for method in ('qr', 'card'):
            self.order()
            self.confirm()
            response = self.pay(method=method, amount='999')
            self.assertContains(response, 'Payment successful')
            sale = Transaction.objects.latest('id')
            references.append(sale.reference)
            self.assertEqual(sale.payment_method, method)
            self.assertEqual(sale.amount_paid, Decimal('279.50'))
            self.assertEqual(sale.change, Decimal('0.00'))
            self.assertContains(self.client.get('/receipt/'), sale.get_payment_method_display())
            self.reset()
        self.assertNotEqual(*references)

    def test_repeated_submit_returns_same_sale_and_immutable_paid_amount(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        for amount in ('300', '300', '500'):
            self.assertContains(self.pay(amount=amount, token=token), 'Payment successful')
            self.assertEqual(Transaction.objects.count(), 1)
            self.assertEqual(TransactionItem.objects.count(), 3)
            self.assertEqual(Transaction.objects.get().amount_paid, Decimal('300.00'))
        Product.objects.filter(pk=self.rice.pk).update(price=Decimal('100.00'))
        self.assertContains(self.pay(token=token), 'Payment successful')
        self.assertEqual(Transaction.objects.get().total, Decimal('279.50'))

    def test_competing_methods_cannot_complete_same_attempt_twice(self):
        self.order()
        self.confirm()
        cash = self.client.get('/payment/cash/').context['payment_token']
        qr = self.client.get('/payment/qr/').context['payment_token']
        stale_session = {'kiosk': deepcopy(self.client.session['kiosk'])}
        self.pay(token=cash)
        with self.assertRaisesMessage(CartError, 'another method'):
            complete_payment(stale_session, 'qr', qr)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_same_attempt_from_two_loaded_sessions_returns_one_sale(self):
        self.order()
        self.confirm()
        state = deepcopy(self.client.session['kiosk'])
        a, b = {'kiosk': deepcopy(state)}, {'kiosk': deepcopy(state)}
        _, token = payment_token(a, 'cash')
        first = complete_payment(a, 'cash', token, '300')
        second = complete_payment(b, 'cash', token, '300')
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_partial_line_failure_rolls_back_header_and_lines(self):
        self.order()
        self.confirm()
        session = {'kiosk': deepcopy(self.client.session['kiosk'])}
        _, token = payment_token(session, 'cash')
        original = TransactionItem.save
        count = 0

        def interrupted(item, *args, **kwargs):
            nonlocal count
            count += 1
            if count == 2:
                raise RuntimeError('Injected write failure for rollback verification')
            return original(item, *args, **kwargs)

        with patch.object(TransactionItem, 'save', interrupted):
            with self.assertRaises(RuntimeError):
                complete_payment(session, 'cash', token, '300')
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(TransactionItem.objects.count(), 0)
        self.assertNotIn('active_reference', session['kiosk'])

    def test_edits_and_catalog_changes_reject_stale_payment(self):
        for change in ('edit', 'price', 'name', 'unavailable', 'delete'):
            with self.subTest(change=change):
                self.order()
                self.confirm()
                token = self.client.get('/payment/cash/').context['payment_token']
                if change == 'edit':
                    self.edit('increase', self.rice)
                elif change == 'price':
                    Product.objects.filter(pk=self.rice.pk).update(price=Decimal('86.00'))
                elif change == 'name':
                    Product.objects.filter(pk=self.rice.pk).update(name='New name')
                elif change == 'unavailable':
                    Product.objects.filter(pk=self.rice.pk).update(is_available=False)
                else:
                    self.drink.delete()
                response = self.pay(token=token)
                self.assertEqual(response.redirect_chain[0], ('/review/', 302))
                self.assertEqual(Transaction.objects.count(), 0)
                self.client = Client()
                Product.objects.filter(pk=self.rice.pk).update(price=Decimal('85.00'),
                                                              name='Chicken Rice Bowl', is_available=True)

    def test_all_unavailable_items_warn_and_require_explicit_repair(self):
        self.edit('add', self.rice)
        saved = deepcopy(self.client.session['kiosk'])
        Product.objects.filter(pk=self.rice.pk).update(is_available=False)
        response = self.review()
        self.assertContains(response, 'Some saved items are invalid or unavailable.')
        self.assertIsNone(response.context['review_token'])
        self.assertEqual(self.client.session['kiosk'], saved)
        self.edit('refresh')
        self.assertContains(self.review(), 'Your order is empty.')

    def test_forged_wrong_method_and_other_customer_tokens_rejected(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        for forged in ('', 'forged', token + 'x'):
            self.assertEqual(self.pay(token=forged).status_code, 400)
        self.assertEqual(self.pay(method='qr', token=token).status_code, 400)
        other = Client()
        self.edit('add', self.rice, client=other)
        reviewed = other.get('/review/').context['review_token']
        other.post('/review/continue/', {'review_token': reviewed})
        response = other.post('/payment/cash/complete/', {'payment_token': token,
                                                         'amount_paid': '300'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_receipt_snapshots_survive_product_edits_and_deletion(self):
        self.order()
        self.confirm()
        self.pay()
        Product.objects.filter(pk=self.rice.pk).update(price=Decimal('100'), name='Changed item')
        self.drink.delete()
        receipt = self.client.get('/receipt/')
        for text in ('Chicken Rice Bowl', 'Cucumber Lemonade', '₱85.00', '₱279.50'):
            self.assertContains(receipt, text)
        self.assertNotContains(receipt, 'Changed item')
        self.assertEqual(TransactionItem.objects.count(), 3)

    def test_reset_rotates_customer_cookie_and_blocks_old_receipt_and_submit(self):
        self.order()
        self.confirm()
        payment_token_value = self.client.get('/payment/cash/').context['payment_token']
        self.pay(token=payment_token_value)
        sale = Transaction.objects.get()
        context = self.client.session['kiosk']['customer_context']
        old_cookie = self.client.cookies['sessionid'].value
        reset_token = self.client.get('/receipt/').context['reset_token']
        session = self.client.session
        session['unrelated'] = 'preserved'
        session.save()
        response = self.reset()
        self.assertContains(response, '₱0.00')
        state = self.client.session['kiosk']
        UUID(state['customer_context'])
        self.assertNotEqual(state['customer_context'], context)
        self.assertNotEqual(self.client.cookies['sessionid'].value, old_cookie)
        self.assertEqual(state['cart'], {})
        self.assertEqual(self.client.session['unrelated'], 'preserved')
        for key in ('active_reference', 'payment_attempt', 'reviewed_order', 'cash_amount'):
            self.assertNotIn(key, state)
        for path in ('/receipt/', f'/receipt/{sale.reference}/', '/success/'):
            self.assertEqual(self.client.get(path).url, '/')
        old_browser = Client()
        old_browser.cookies['sessionid'] = old_cookie
        self.assertEqual(old_browser.get(f'/receipt/{sale.reference}/').url, '/')
        self.assertEqual(self.pay(token=payment_token_value).redirect_chain[0], ('/review/', 302))
        self.edit('add', self.wrap)
        current = deepcopy(self.client.session['kiosk'])
        self.client.post('/new-transaction/', {'reset_token': reset_token})
        self.assertEqual(self.client.session['kiosk'], current)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_other_session_cannot_read_receipt_or_success(self):
        self.order()
        self.confirm()
        self.pay()
        sale = Transaction.objects.get()
        other = Client()
        for path in ('/receipt/', f'/receipt/{sale.reference}/', '/success/'):
            self.assertEqual(other.get(path).url, '/')

    def test_completed_customer_cannot_edit_until_new_transaction(self):
        self.order()
        self.confirm()
        self.pay()
        before = deepcopy(self.client.session['kiosk'])
        for path in ('/', '/review/'):
            self.assertEqual(self.client.get(path).url, '/receipt/')
        self.assertEqual(self.edit('add', self.wrap).url, '/receipt/')
        response = self.client.post('/cart/', {'action': 'add', 'product_id': self.wrap.pk},
                                    HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'redirect': '/receipt/'})
        self.assertEqual(self.client.session['kiosk'], before)

    def test_second_customer_has_distinct_reference_and_own_items(self):
        self.order()
        self.confirm()
        self.pay()
        first = Transaction.objects.get()
        self.reset()
        self.edit('add', self.wrap)
        self.confirm()
        self.pay(method='card')
        second = Transaction.objects.latest('id')
        self.assertNotEqual(first.reference, second.reference)
        self.assertNotEqual(first.customer_context, second.customer_context)
        self.assertEqual(second.total, Decimal('70.00'))
        self.assertEqual(second.items.count(), 1)
        receipt = self.client.get('/receipt/')
        self.assertNotContains(receipt, first.reference)
        self.assertNotContains(receipt, 'Chicken Rice Bowl')
        self.assertEqual(Transaction.objects.count(), 2)

    def test_post_boundaries_and_enforced_csrf(self):
        for url in ('/review/continue/', '/payment/cash/complete/', '/new-transaction/'):
            self.assertEqual(self.client.get(url).status_code, 405)
        guarded = Client(enforce_csrf_checks=True)
        guarded.get('/')
        csrf = guarded.cookies['csrftoken'].value
        guarded.post('/cart/', {'action': 'add', 'product_id': self.rice.pk,
                               'csrfmiddlewaretoken': csrf})
        token = guarded.get('/review/').context['review_token']
        self.assertEqual(guarded.post('/review/continue/', {'review_token': token}).status_code, 403)
        guarded.post('/review/continue/', {'review_token': token, 'csrfmiddlewaretoken': csrf})
        token = guarded.get('/payment/cash/').context['payment_token']
        self.assertEqual(guarded.post('/payment/cash/complete/', {'payment_token': token,
                                                                'amount_paid': '85'}).status_code, 403)
        guarded.post('/payment/cash/complete/', {'payment_token': token, 'amount_paid': '85',
                                                'csrfmiddlewaretoken': csrf})
        reset = guarded.get('/receipt/').context['reset_token']
        self.assertEqual(guarded.post('/new-transaction/', {'reset_token': reset}).status_code, 403)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_damaged_metadata_and_oversize_orders_do_not_advance(self):
        self.order()
        original = deepcopy(self.client.session['kiosk'])
        for field, value in (('customer_context', None), ('revision', True), ('revision', -1)):
            saved = deepcopy(original)
            saved[field] = value
            session = self.client.session
            session['kiosk'] = saved
            session.save()
            self.assertIsNone(self.review().context['review_token'])
            self.assertEqual(self.client.get('/payment/').url, '/review/')
        session = self.client.session
        saved = deepcopy(original)
        saved['cart'] = {str(self.rice.pk): 99, str(self.wrap.pk): 99}
        session['kiosk'] = saved
        session.save()
        Product.objects.filter(pk__in=(self.rice.pk, self.wrap.pk)).update(price=Decimal('999999.99'))
        response = self.review()
        self.assertTrue(response.context['order']['over_limit'])
        self.assertIsNone(response.context['review_token'])
        self.assertEqual(Transaction.objects.count(), 0)


class ConcurrentCompletionTests(TransactionTestCase):
    def test_parallel_same_attempt_creates_only_one_complete_sale(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        from django.db import connections
        from .cart import calculate_order, change_cart
        from .checkout import REVIEW_SIGNER, confirm_order, order_facts

        call_command('seed_catalog', verbosity=0)
        product = Product.objects.get(seed_key='rice-bowl')
        session = {}
        change_cart(session, 'add', str(product.pk))
        facts = order_facts(session['kiosk'], calculate_order(session['kiosk']['cart']))
        confirm_order(session, REVIEW_SIGNER.sign_object(facts))
        _, token = payment_token(session, 'cash')
        copies = [deepcopy(session), deepcopy(session)]
        start = Barrier(2)

        def worker(copy):
            try:
                start.wait(timeout=5)
                return complete_payment(copy, 'cash', token, '100').reference
            except CartError as error:
                # SQLite contention may reject one attempt; an explicit retry is safe.
                self.assertIn('busy', str(error))
                return None
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(worker, copies))
        retries = [complete_payment(copy, 'cash', token, '100').reference for copy in copies]
        self.assertEqual(len(set(retries)), 1)
        self.assertTrue(all(result is None or result == retries[0] for result in outcomes))
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(TransactionItem.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().change, Decimal('15.00'))
