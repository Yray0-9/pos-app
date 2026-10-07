"""Persistent catalog and completed sales; active carts belong to sessions."""

from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


MAX_UNIT_PRICE = Decimal('999999.99')
MAX_AMOUNT = Decimal('99999999.99')
MAX_QUANTITY = 99


def new_reference():
    return f'CT-{uuid4().hex}'


class Product(models.Model):
    seed_key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=160, blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=Decimal('0.01'), price__lte=MAX_UNIT_PRICE),
                name='product_price_range',
            ),
        ]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Only completed sales are stored here; there is no pending-sale state."""

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        QR = 'qr', 'QR Payment'
        CARD = 'card', 'Credit/Debit Card'

    reference = models.CharField(
        max_length=35, default=new_reference, unique=True, editable=False,
        validators=[RegexValidator(r'^CT-[0-9a-f]{32}$', 'Invalid transaction reference.')],
    )
    # Supplied by the future reviewed-order/session flow, never regenerated on retry.
    payment_attempt = models.UUIDField(unique=True, editable=False)
    customer_context = models.UUIDField(editable=False)
    completed_at = models.DateTimeField(default=timezone.now, editable=False)
    payment_method = models.CharField(max_length=4, choices=PaymentMethod.choices)
    total = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    change = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )

    class Meta:
        ordering = ['-completed_at', '-id']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(payment_method__in=['cash', 'qr', 'card']),
                name='sale_payment_method_valid',
            ),
            models.CheckConstraint(
                condition=models.Q(total__gte=Decimal('0.01'), total__lte=MAX_AMOUNT),
                name='sale_total_range',
            ),
            models.CheckConstraint(
                condition=models.Q(amount_paid__gte=models.F('total'), amount_paid__lte=MAX_AMOUNT),
                name='sale_paid_covers_total',
            ),
            models.CheckConstraint(
                condition=models.Q(change__gte=Decimal('0.00'), change__lte=MAX_AMOUNT),
                name='sale_change_range',
            ),
            models.CheckConstraint(
                condition=(models.Q(payment_method='cash') | models.Q(
                    amount_paid=models.F('total'), change=Decimal('0.00'),
                )),
                name='sale_noncash_exact_payment',
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}
        for field in ('payment_attempt', 'customer_context', 'reference', 'completed_at'):
            if getattr(self, field) in (None, ''):
                errors[field] = 'This completed-sale value is required.'
        amounts = (self.total, self.amount_paid, self.change)
        # full_clean() still calls clean() after field errors; leave malformed values
        # to DecimalField instead of raising arithmetic errors while reporting them.
        if not all(isinstance(value, Decimal) and value.is_finite() for value in amounts):
            if errors:
                raise ValidationError(errors)
            return
        if self.amount_paid < self.total:
            errors['amount_paid'] = 'Payment must cover the total.'
        if self.change != self.amount_paid - self.total:
            errors['change'] = 'Change must equal amount paid minus total.'
        if self.payment_method in (self.PaymentMethod.QR, self.PaymentMethod.CARD):
            if self.amount_paid != self.total or self.change != Decimal('0.00'):
                errors['amount_paid'] = 'QR/card payment must equal the total, with zero change.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.reference


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_items',
    )
    product_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_QUANTITY)],
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1, quantity__lte=MAX_QUANTITY),
                name='sale_item_quantity_range',
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=Decimal('0.01'), unit_price__lte=MAX_UNIT_PRICE),
                name='sale_item_price_range',
            ),
            models.CheckConstraint(
                condition=models.Q(subtotal__gte=Decimal('0.01'), subtotal__lte=MAX_AMOUNT),
                name='sale_item_subtotal_range',
            ),
        ]

    def clean(self):
        super().clean()
        if (isinstance(self.unit_price, Decimal) and self.unit_price.is_finite()
                and isinstance(self.subtotal, Decimal) and self.subtotal.is_finite()
                and isinstance(self.quantity, int)):
            if self.subtotal != self.unit_price * self.quantity:
                raise ValidationError({'subtotal': 'Subtotal must equal unit price times quantity.'})

    def __str__(self):
        return f'{self.quantity} x {self.product_name}'
