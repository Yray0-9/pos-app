"""Current database-free acceptance; SimpleTestCase forbids database queries."""
from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
from unittest.mock import patch

from django.conf import settings
from django.test import Client, SimpleTestCase

from . import catalog
from .cart import CartError, calculate_order
from .checkout import complete_payment, owned_sale, payment_token


class KioskFlowTests(SimpleTestCase):
    def act(self, action='add', identifier='1', client=None, **extra):
        return (client or self.client).post('/cart/',
            {'action': action, 'product_id': identifier, **extra}, HTTP_ACCEPT='application/json')

    def state(self):
        return self.client.session.get('kiosk', {})

    def save(self, state):
        session = self.client.session
        session['kiosk'] = state
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    def order(self):
        for identifier in ('1', '1', '2', '3'):
            self.assertEqual(self.act(identifier=identifier).status_code, 200)

    def confirm(self):
        review = self.client.get('/review/')
        return self.client.post('/review/continue/', {'review_token': review.context['review_token']})

    def pay(self, method='cash', amount='300', token=None):
        token = token or self.client.get(f'/payment/{method}/').context['payment_token']
        return self.client.post(f'/payment/{method}/complete/',
            {'payment_token': token, 'amount_paid': amount, 'total': '0.01'}, follow=True)

    def reset(self):
        token = self.client.get('/receipt/').context['reset_token']
        return self.client.post('/new-transaction/', {'reset_token': token}, follow=True)

    def test_database_free_catalog_and_empty_guards(self):
        self.assertEqual(settings.SESSION_ENGINE, 'django.contrib.sessions.backends.signed_cookies')
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.dummy')
        page = self.client.get('/')
        self.assertEqual(len(page.context['catalog']), 6)
        for product in catalog.PRODUCTS:
            self.assertContains(page, product.name)
            self.assertContains(page, f'₱{product.price:.2f}')
        self.assertEqual(page.context['order']['total'], Decimal('0.00'))
        self.assertContains(self.client.get('/review/'), 'Your order is empty.')
        for url in ('/payment/', '/payment/qr/', '/success/', '/receipt/'):
            self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(self.client.post('/review/continue/', {'review_token': 'bad'}).url, '/review/')

    def test_cart_arithmetic_quantity_and_explicit_removal(self):
        self.order()
        order = calculate_order(self.state()['cart'])
        self.assertEqual(order['total'], Decimal('279.50'))
        self.assertEqual([x['subtotal'] for x in order['lines']],
                         [Decimal('170.00'), Decimal('70.00'), Decimal('39.50')])
        for action, identifier, total in (
            ('increase', '1', '364.50'), ('decrease', '1', '279.50'),
            ('remove', '3', '240.00'), ('decrease', '2', '170.00'), ('remove', '1', '0.00')):
            self.act(action, identifier)
            self.assertEqual(calculate_order(self.state()['cart'])['total'], Decimal(total))
        self.assertEqual(self.act('decrease', '1').status_code, 400)

    def test_invalid_inputs_do_not_mutate_and_browser_prices_ignored(self):
        self.act(price='0.01', quantity='-9', subtotal='0')
        saved = deepcopy(self.state())
        self.assertEqual(calculate_order(saved['cart'])['total'], Decimal('85.00'))
        for identifier in ('', '0', '-1', '01', '1.5', 'NaN', '１', '9999', '9' * 30):
            with self.subTest(identifier=identifier):
                self.assertEqual(self.act(identifier=identifier).status_code, 400)
                self.assertEqual(self.state(), saved)
        for action in ('set', 'pay', '', 'refresh'):
            self.assertEqual(self.act(action).status_code, 400)
        self.assertEqual(self.state(), saved)

    def test_quantity_limit_and_corrupt_cart_repair(self):
        self.save({'cart': {'1': 98}})
        self.act()
        self.assertEqual(self.state()['cart']['1'], 99)
        self.assertEqual(self.act().status_code, 400)
        self.act('decrease')
        self.assertEqual(self.state()['cart']['1'], 98)
        for bad in (-1, 0, 100, True, 1.5, '2', None):
            self.save({'cart': {'1': bad, '2': 2, '-1': 1}})
            self.assertTrue(self.client.get('/').context['order']['needs_refresh'])
            self.assertEqual(self.act('refresh', '').status_code, 200)
            self.assertEqual(self.state()['cart'], {'2': 2})
        for raw in (None, [], 'broken'):
            self.save({'cart': raw})
            self.assertTrue(self.client.get('/').context['order']['needs_refresh'])
            self.act('refresh', '')
            self.assertEqual(self.state()['cart'], {})

    def test_review_back_and_edits_preserve_recalculate(self):
        self.order()
        saved = deepcopy(self.state())
        for _ in range(3):
            page = self.client.get('/review/')
            self.assertEqual(page.context['order']['total'], Decimal('279.50'))
            self.assertContains(page, 'Back to selection')
            self.client.get('/')
            self.assertEqual(self.state(), saved)
        old = page.context['review_token']
        self.act('increase')
        response = self.client.post('/review/continue/', {'review_token': old}, follow=True)
        self.assertContains(response, 'Your order changed.')
        self.assertEqual(response.context['order']['total'], Decimal('364.50'))
        self.assertEqual(self.confirm().url, '/payment/')

    def test_missing_unavailable_product_is_warned_not_silently_paid(self):
        self.order()
        saved = deepcopy(self.state())
        products = tuple(replace(x, is_available=False) if x.pk == 1 else x
                         for x in catalog.PRODUCTS if x.pk != 3)
        with patch.object(catalog, 'PRODUCTS', products):
            review = self.client.get('/review/')
            self.assertContains(review, 'Some saved items are invalid or unavailable.')
            self.assertIsNone(review.context['review_token'])
            self.assertEqual(self.state(), saved)
            self.assertEqual(self.act().status_code, 400)
            self.act('refresh', '')
            self.assertEqual(self.state()['cart'], {'2': 1})

    def test_all_payment_choices_and_visible_instructions(self):
        self.order()
        self.confirm()
        page = self.client.get('/payment/')
        for name in ('Cash', 'QR Payment', 'Credit/Debit Card'):
            self.assertContains(page, name)
        for method, text in (('cash', 'Cash amount received'), ('qr', 'DEMO PLACEHOLDER'),
                             ('card', 'Tap, insert or swipe your card')):
            self.assertContains(self.client.get(f'/payment/{method}/'), text)
        self.assertEqual(self.client.get('/payment/unknown/').url, '/review/')

    def test_cash_errors_leave_no_receipt_and_keep_cart(self):
        self.order()
        self.confirm()
        saved = deepcopy(self.state())
        for amount in ('', 'abc', 'NaN', 'Infinity', '-1', '0', '279.49', '1.234',
                       '1e3', '100,000', '100000000'):
            with self.subTest(amount=amount):
                response = self.pay(amount=amount)
                self.assertEqual(response.status_code, 400)
                self.assertContains(response, 'Please check:', status_code=400)
                self.assertEqual(self.state(), saved)
                self.assertIsNone(owned_sale(self.state()))

    def test_exact_and_excess_cash_receipt_fields_and_timestamp(self):
        for amount, change in (('279.50', '0.00'), ('300', '20.50')):
            self.order()
            self.confirm()
            self.assertContains(self.pay(amount=amount), 'Payment successful')
            sale = owned_sale(self.state())
            self.assertEqual((sale.total, sale.amount_paid, sale.change),
                             (Decimal('279.50'), Decimal(amount), Decimal(change)))
            self.assertEqual(sum(x.subtotal for x in sale.items), sale.total)
            page = self.client.get('/receipt/')
            for text in (sale.reference, 'Asia/Singapore', 'Oct', '2026', 'Chicken Rice Bowl',
                         'Quantity 2', '₱85.00', '₱170.00', '₱279.50', f'₱{change}'):
                self.assertContains(page, text)
            self.assertIsNotNone(sale.completed_at.utcoffset())
            self.reset()

    def test_qr_card_receipts_and_distinct_references(self):
        references = []
        for method in ('qr', 'card'):
            self.order()
            self.confirm()
            self.assertContains(self.pay(method, amount='999'), 'Payment successful')
            sale = owned_sale(self.state())
            self.assertEqual(sale.amount_paid, Decimal('279.50'))
            self.assertEqual(sale.change, Decimal('0.00'))
            self.assertEqual(sale.payment_method, method)
            self.assertContains(self.client.get('/receipt/'), sale.get_payment_method_display())
            references.append(sale.reference)
            self.reset()
        self.assertNotEqual(*references)

    def test_serial_duplicate_retains_snapshot_and_paid_amount(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        self.pay(token=token)
        saved = deepcopy(self.state()['receipt'])
        for amount in ('300', '500'):
            self.pay(token=token, amount=amount)
            self.assertEqual(self.state()['receipt'], saved)
        products = tuple(replace(x, price=Decimal('100.00'), name='Changed') if x.pk == 1 else x
                         for x in catalog.PRODUCTS)
        with patch.object(catalog, 'PRODUCTS', products):
            self.pay(token=token)
            self.assertEqual(self.state()['receipt'], saved)
            self.assertContains(self.client.get('/receipt/'), 'Chicken Rice Bowl')

    def test_current_cookie_rejects_alternate_method_after_completion(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/qr/').context['payment_token']
        self.pay()
        saved = deepcopy(self.state()['receipt'])
        session = {'kiosk': deepcopy(self.state())}
        with self.assertRaisesMessage(CartError, 'another method'):
            complete_payment(session, 'qr', token)
        self.assertEqual(session['kiosk']['receipt'], saved)

    def test_two_precompletion_copies_have_stable_reference_without_global_lock(self):
        self.order()
        self.confirm()
        a, b = ({'kiosk': deepcopy(self.state())} for _ in range(2))
        _, token = payment_token(a, 'cash')
        first = complete_payment(a, 'cash', token, '300')
        second = complete_payment(b, 'cash', token, '500')
        self.assertEqual(first.reference, second.reference)
        # Explicit architectural limit: separate old cookies can choose different cash.
        self.assertNotEqual(first.amount_paid, second.amount_paid)

    def test_stale_catalog_price_or_cart_cannot_pay(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        products = tuple(replace(x, price=Decimal('86.00')) if x.pk == 1 else x
                         for x in catalog.PRODUCTS)
        with patch.object(catalog, 'PRODUCTS', products):
            response = self.pay(token=token)
            self.assertEqual(response.redirect_chain[0], ('/review/', 302))
            self.assertIsNone(owned_sale(self.state()))
        self.act('increase')
        response = self.pay(token=token)
        self.assertEqual(response.redirect_chain[0], ('/review/', 302))

    def test_forged_and_cross_customer_tokens_and_cookie_rejected(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        for forged in ('bad', token + 'x'):
            self.assertEqual(self.pay(token=forged).status_code, 400)
        self.assertEqual(self.pay('qr', token=token).status_code, 400)
        other = Client()
        for identifier in ('1', '1', '2', '3'):
            self.act(identifier=identifier, client=other)
        review = other.get('/review/').context['review_token']
        other.post('/review/continue/', {'review_token': review})
        self.assertEqual(other.post('/payment/cash/complete/',
            {'payment_token': token, 'amount_paid': '300'}).status_code, 400)
        other.cookies[settings.SESSION_COOKIE_NAME] = self.client.cookies[settings.SESSION_COOKIE_NAME].value + 'x'
        self.assertEqual(other.get('/').context['order']['cart'], {})

    def test_reset_clears_current_state_and_ordinary_old_links_are_denied(self):
        self.order()
        self.confirm()
        token = self.client.get('/payment/cash/').context['payment_token']
        self.pay(token=token)
        reference = owned_sale(self.state()).reference
        context = self.state()['customer_context']
        self.assertEqual(Client().get(f'/receipt/{reference}/').url, '/')
        self.assertEqual(self.client.get('/').url, '/receipt/')
        self.assertEqual(self.act().status_code, 409)
        page = self.reset()
        self.assertEqual(page.context['order']['cart'], {})
        self.assertEqual(page.context['order']['total'], Decimal('0.00'))
        self.assertNotEqual(context, self.state()['customer_context'])
        self.assertNotIn('receipt', self.state())
        self.assertEqual(self.client.get(f'/receipt/{reference}/').url, '/')
        self.assertEqual(self.pay(token=token).redirect_chain[0], ('/review/', 302))

    def test_copied_old_signed_cookie_replay_limitation_is_explicit(self):
        self.order()
        self.confirm()
        self.pay()
        old_cookie = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.reset()
        copied = Client()
        copied.cookies[settings.SESSION_COOKIE_NAME] = old_cookie
        # No shared database means logout/reset cannot revoke a copied prior cookie.
        self.assertEqual(copied.get('/receipt/').status_code, 200)

    def test_maximum_catalog_receipt_cookie_fits_browser_limit(self):
        self.save({'cart': {str(x.pk): 99 for x in catalog.PRODUCTS}, 'revision': 1,
                   'customer_context': '9834a049-c8ec-4b49-ab21-8015a3b4feb8'})
        self.confirm()
        response = self.pay('qr')
        cookie = response.cookies.get(settings.SESSION_COOKIE_NAME) or self.client.cookies[settings.SESSION_COOKIE_NAME]
        self.assertLess(len(cookie.output().encode()), 4096)
        self.assertEqual(len(owned_sale(self.state()).items), 6)

    def test_malformed_active_receipt_is_not_rendered(self):
        self.order()
        self.confirm()
        self.pay()
        original = deepcopy(self.state())
        for key, value in (('total', 'NaN'), ('amount_paid', '-1'), ('items', []),
                           ('completed_at', 'invalid'), ('reference', 'other')):
            state = deepcopy(original)
            state['receipt'][key] = value
            self.assertIsNone(owned_sale(state))

    def test_csrf_post_methods_and_no_store_headers(self):
        protected = Client(enforce_csrf_checks=True)
        for path in ('/cart/', '/review/continue/', '/payment/cash/complete/', '/new-transaction/'):
            self.assertEqual(protected.post(path).status_code, 403)
            self.assertEqual(self.client.get(path).status_code, 405)
        page = protected.get('/')
        self.assertIn('no-store', page.headers['Cache-Control'])
        token = protected.cookies['csrftoken'].value
        response = protected.post('/cart/', {'action': 'add', 'product_id': '1',
                                              'csrfmiddlewaretoken': token}, follow=True)
        self.assertEqual(response.context['order']['total'], Decimal('85.00'))

    def test_user_text_is_escaped_and_all_unavailable_empty_state(self):
        products = tuple(replace(x, name='<script>alert(1)</script>') if x.pk == 1 else x
                         for x in catalog.PRODUCTS)
        with patch.object(catalog, 'PRODUCTS', products):
            self.assertContains(self.client.get('/'), '&lt;script&gt;alert(1)&lt;/script&gt;')
            self.assertNotContains(self.client.get('/'), '<script>alert(1)</script>')
        with patch.object(catalog, 'PRODUCTS', ()):
            self.assertContains(self.client.get('/'), 'No items are available right now')
