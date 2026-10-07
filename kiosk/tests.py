"""Data integrity checks; test sales stay in Django's separate test database."""

from decimal import Decimal
from io import StringIO
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone

from .models import Product, Transaction, TransactionItem


class CatalogAndSaleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', stdout=StringIO())

    def sale(self, **changes):
        values = {
            'payment_attempt': uuid4(), 'customer_context': uuid4(),
            'payment_method': Transaction.PaymentMethod.CASH,
            'total': Decimal('279.50'), 'amount_paid': Decimal('300.00'),
            'change': Decimal('20.50'),
        }
        values.update(changes)
        sale = Transaction(**values)
        sale.full_clean()
        sale.save()
        return sale

    def item(self, sale, **changes):
        product = Product.objects.get(seed_key='rice-bowl')
        values = {
            'transaction': sale, 'product': product, 'product_name': product.name,
            'unit_price': product.price, 'quantity': 2, 'subtotal': Decimal('170.00'),
        }
        values.update(changes)
        item = TransactionItem(**values)
        item.full_clean()
        item.save()
        return item

    def test_seed_matches_agreed_catalog_and_preserves_ids(self):
        expected = {
            'Chicken Rice Bowl': Decimal('85.00'), 'Chicken Wrap': Decimal('70.00'),
            'Cucumber Lemonade': Decimal('39.50'), 'Banana Muffin': Decimal('34.50'),
            'Cheese Bun': Decimal('29.50'), 'Granola Pack': Decimal('24.00'),
        }
        self.assertEqual(dict(Product.objects.values_list('name', 'price')), expected)
        before = list(Product.objects.values_list('seed_key', 'id'))
        output = StringIO()
        call_command('seed_catalog', stdout=output)
        self.assertEqual(list(Product.objects.values_list('seed_key', 'id')), before)
        self.assertIn('0 created, 6 preserved', output.getvalue())
        self.assertTrue(all(isinstance(p.price, Decimal) and p.is_available for p in Product.objects.all()))

    def test_seed_preserves_existing_edits_and_unrelated_products(self):
        product = Product.objects.get(seed_key='rice-bowl')
        product.name = 'My edited bowl'
        product.price = Decimal('90.00')
        product.is_available = False
        product.save()
        Product.objects.create(seed_key='extra', name='Extra product', price=Decimal('1.00'))
        call_command('seed_catalog', stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual((product.name, product.price, product.is_available), ('My edited bowl', Decimal('90.00'), False))
        self.assertEqual(Product.objects.count(), 7)

    def test_money_roundtrip_and_agreed_order_arithmetic_are_exact(self):
        prices = dict(Product.objects.values_list('seed_key', 'price'))
        total = prices['rice-bowl'] * 2 + prices['chicken-wrap'] + prices['cucumber-lemonade']
        self.assertEqual(total, Decimal('279.50'))
        self.assertEqual(total + prices['rice-bowl'], Decimal('364.50'))
        self.assertEqual(total - prices['cucumber-lemonade'], Decimal('240.00'))
        sale = self.sale(total=total)
        sale.refresh_from_db()
        self.assertEqual(sale.amount_paid - sale.total, sale.change)
        small = self.sale(total=Decimal('0.10') + Decimal('0.20'), amount_paid=Decimal('1.00'), change=Decimal('0.70'))
        small.refresh_from_db()
        self.assertEqual((small.total, small.change), (Decimal('0.30'), Decimal('0.70')))
        self.assertEqual(f'{small.total:.2f}', '0.30')

    def test_references_attempts_and_contexts_are_distinct(self):
        first, second = self.sale(), self.sale()
        self.assertNotEqual(first.reference, second.reference)
        self.assertRegex(first.reference, r'^CT-[0-9a-f]{32}$')
        self.assertNotEqual(first.payment_attempt, second.payment_attempt)
        self.assertNotEqual(first.customer_context, second.customer_context)
        self.assertTrue(timezone.is_aware(first.completed_at))

    def test_database_rejects_duplicate_attempt_and_reference(self):
        original = self.sale()
        for unique_field in ('payment_attempt', 'reference'):
            with self.subTest(field=unique_field), self.assertRaises(IntegrityError), transaction.atomic():
                Transaction.objects.create(
                    payment_attempt=original.payment_attempt if unique_field == 'payment_attempt' else uuid4(),
                    reference=original.reference if unique_field == 'reference' else f'CT-{uuid4().hex}',
                    customer_context=uuid4(), payment_method='cash', total=Decimal('1.00'),
                    amount_paid=Decimal('1.00'), change=Decimal('0.00'),
                )
        self.assertEqual(Transaction.objects.count(), 1)

    def test_non_cash_methods_require_exact_total_and_zero_change(self):
        for method in ('qr', 'card'):
            with self.subTest(method=method):
                sale = self.sale(payment_method=method, amount_paid=Decimal('279.50'), change=Decimal('0.00'))
                self.assertEqual(sale.get_payment_method_display(), 'QR Payment' if method == 'qr' else 'Credit/Debit Card')
                with self.assertRaises(ValidationError):
                    self.sale(payment_method=method)
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Transaction.objects.create(
                        payment_attempt=uuid4(), customer_context=uuid4(), payment_method=method,
                        total=Decimal('1.00'), amount_paid=Decimal('2.00'), change=Decimal('1.00'),
                    )

    def test_cash_exact_and_excess_validate_but_insufficient_or_wrong_change_do_not(self):
        self.sale(amount_paid=Decimal('279.50'), change=Decimal('0.00'))
        self.sale()
        for changes in ({'amount_paid': Decimal('200.00')}, {'change': Decimal('21.00')}):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                self.sale(**changes)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_product_rejects_invalid_money_before_save(self):
        for price in ('0.00', '-1.00', '1.234', '1000000.00', 'NaN', 'Infinity', 'not-money'):
            with self.subTest(price=price), self.assertRaises(ValidationError):
                Product(seed_key='invalid', name='Invalid', price=price).full_clean()

    def test_sale_rejects_invalid_method_missing_context_and_invalid_amount(self):
        for changes in (
            {'payment_method': 'bank'}, {'customer_context': None}, {'payment_attempt': None},
            {'reference': ''}, {'completed_at': None},
            {'total': Decimal('0.00')}, {'amount_paid': Decimal('300.001')},
            {'change': Decimal('-0.01')}, {'amount_paid': Decimal('NaN')},
            {'amount_paid': Decimal('100000000.00')},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                self.sale(**changes)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_item_snapshots_survive_catalog_edits_and_product_deletion(self):
        sale = self.sale()
        item = self.item(sale)
        product = item.product
        product.name, product.price = 'Renamed product', Decimal('99.00')
        product.save()
        item.refresh_from_db()
        self.assertEqual((item.product_name, item.unit_price, item.subtotal), ('Chicken Rice Bowl', Decimal('85.00'), Decimal('170.00')))
        product.delete()
        item.refresh_from_db()
        self.assertIsNone(item.product_id)
        self.assertEqual(item.product_name, 'Chicken Rice Bowl')
        self.assertTrue(Transaction.objects.filter(pk=sale.pk).exists())

    def test_item_rejects_invalid_quantity_and_inconsistent_subtotal(self):
        sale = self.sale()
        for quantity in (0, -1, 100):
            with self.subTest(quantity=quantity), self.assertRaises(ValidationError):
                self.item(sale, quantity=quantity)
        with self.assertRaises(ValidationError):
            self.item(sale, subtotal=Decimal('169.99'))
        self.assertEqual(sale.items.count(), 0)

    def test_database_guards_invalid_values_even_without_full_clean(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(seed_key='zero', name='Zero', price=Decimal('0.00'))
        sale = self.sale()
        with self.assertRaises(IntegrityError), transaction.atomic():
            TransactionItem.objects.create(
                transaction=sale, product_name='Invalid', unit_price=Decimal('1.00'),
                quantity=0, subtotal=Decimal('1.00'),
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            Transaction.objects.create(
                payment_attempt=uuid4(), customer_context=uuid4(), payment_method='bank',
                total=Decimal('1.00'), amount_paid=Decimal('1.00'), change=Decimal('0.00'),
            )

    def test_completed_sale_with_items_is_protected_from_accidental_deletion(self):
        sale = self.sale()
        self.item(sale)
        with self.assertRaises(ProtectedError):
            sale.delete()

    def test_atomic_sale_item_writes_roll_back_together_on_failure(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            sale = self.sale()
            self.item(sale)
            TransactionItem.objects.create(
                transaction=sale, product_name='Invalid', unit_price=Decimal('1.00'),
                quantity=0, subtotal=Decimal('1.00'),
            )
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(TransactionItem.objects.count(), 0)
