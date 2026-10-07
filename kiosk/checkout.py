"""Review binding and one trusted completion path for all simulated payments."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
import re
from uuid import UUID, uuid4

from django.core import signing
from django.utils import timezone

from .cart import CartError, calculate_order, cart_state
from .catalog import MAX_AMOUNT, MAX_QUANTITY


REVIEW_SIGNER = signing.Signer(salt='kiosk.review')
PAYMENT_SIGNER = signing.Signer(salt='kiosk.payment')
RESET_SIGNER = signing.Signer(salt='kiosk.reset')
METHODS = {'cash': 'Cash', 'qr': 'QR Payment', 'card': 'Credit/Debit Card'}


def uuid_value(value):
    try:
        return str(UUID(str(value)))
    except ValueError:
        raise CartError('Your order session needs refreshing. Go back and adjust an item.') from None


def order_facts(state, order):
    if order['needs_refresh']:
        raise CartError('Some saved items are invalid or unavailable. Go back and update your order.')
    if not order['lines']:
        raise CartError('Your order is empty. Add an item before continuing.')
    if order['over_limit']:
        raise CartError('Your total is too large. Go back and reduce your order.')
    context = uuid_value(state.get('customer_context'))
    revision = state.get('revision')
    if type(revision) is not int or revision < 1:
        raise CartError('Your order session needs refreshing. Go back and adjust an item.')
    return {'customer_context': context, 'revision': revision,
            'items': [{'product_id': line['product'].pk, 'name': line['product'].name,
                       'unit_price': format(line['unit_price'], '.2f'),
                       'quantity': line['quantity'], 'subtotal': format(line['subtotal'], '.2f')}
                      for line in order['lines']], 'total': format(order['total'], '.2f')}


def unsigned(signer, token):
    try:
        value = signer.unsign_object(token)
    except (signing.BadSignature, ValueError, TypeError):
        raise CartError('This confirmation is no longer valid. Please review your order again.') from None
    if not isinstance(value, dict):
        raise CartError('Please review your order again.')
    return value


def confirm_order(session, token):
    state = cart_state(session)
    facts = order_facts(state, calculate_order(state.get('cart', {})))
    if unsigned(REVIEW_SIGNER, token) != facts:
        raise CartError('Your order changed. Check the updated order before continuing.')
    attempt = state.get('payment_attempt')
    try:
        attempt = uuid_value(attempt)
    except CartError:
        attempt = None
    if state.get('reviewed_order') != facts or attempt is None:
        attempt = str(uuid4())
    updated = state.copy()
    updated.update(reviewed_order=facts, payment_attempt=attempt)
    session['kiosk'] = updated


def payment_order(session):
    state = cart_state(session)
    order = calculate_order(state.get('cart', {}))
    facts = order_facts(state, order)
    if facts != state.get('reviewed_order'):
        raise CartError('Your order changed or has not been reviewed. Please review it again.')
    attempt = uuid_value(state.get('payment_attempt'))
    return state, order, {'facts': facts, 'attempt': attempt}


def payment_token(session, method):
    _, order, payload = payment_order(session)
    if method not in METHODS:
        raise CartError('Choose Cash, QR Payment or Credit/Debit Card.')
    return order, PAYMENT_SIGNER.sign_object({**payload, 'method': method})


def cash_value(raw, total):
    text = raw.strip() if isinstance(raw, str) else ''
    if not text:
        raise CartError('Enter the cash amount received.')
    if not re.fullmatch(r'[0-9]{1,8}(?:\.[0-9]{1,2})?', text):
        raise CartError('Enter a positive cash amount using digits and up to two decimal places.')
    paid = Decimal(text).quantize(Decimal('0.01'))
    if paid > MAX_AMOUNT:
        raise CartError('The cash amount exceeds the supported limit.')
    if paid < total:
        raise CartError(f'Insufficient cash. The amount due is PHP {total:.2f}.')
    return paid


@dataclass(frozen=True)
class SaleItem:
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal


@dataclass(frozen=True)
class Sale:
    reference: str
    customer_context: str
    payment_attempt: str
    payment_method: str
    total: Decimal
    amount_paid: Decimal
    change: Decimal
    completed_at: datetime
    items: tuple

    def get_payment_method_display(self):
        return METHODS[self.payment_method]


def stored_money(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{1,8}\.[0-9]{2}', value):
        raise ValueError('Invalid receipt money')
    amount = Decimal(value)
    if not amount.is_finite() or not Decimal('0.00') <= amount <= MAX_AMOUNT:
        raise ValueError('Invalid receipt money')
    return amount


def owned_sale(state):
    """Read the active snapshot from the authenticated cookie; no sales ledger."""
    raw = state.get('receipt')
    if not isinstance(raw, dict):
        return None
    try:
        context = uuid_value(state.get('customer_context'))
        attempt = uuid_value(state.get('payment_attempt'))
        reference = 'CT-' + UUID(attempt).hex
        if (raw['reference'] != reference or state.get('active_reference') != reference
                or raw['customer_context'] != context or raw['payment_attempt'] != attempt
                or raw['payment_method'] not in METHODS):
            return None
        if not isinstance(raw['items'], list) or not 1 <= len(raw['items']) <= 6:
            return None
        items = []
        for line in raw['items']:
            quantity = line['quantity']
            name = line['product_name']
            if (type(quantity) is not int or not 1 <= quantity <= MAX_QUANTITY
                    or not isinstance(name, str) or not 1 <= len(name) <= 120):
                return None
            unit, subtotal = stored_money(line['unit_price']), stored_money(line['subtotal'])
            if unit <= 0 or unit * quantity != subtotal:
                return None
            items.append(SaleItem(name, unit, quantity, subtotal))
        total, paid, change = (stored_money(raw[key]) for key in ('total', 'amount_paid', 'change'))
        if (total != sum((item.subtotal for item in items), Decimal('0.00'))
                or total <= 0 or paid < total or paid - total != change
                or (raw['payment_method'] != 'cash' and (paid != total or change != 0))):
            return None
        completed_at = datetime.fromisoformat(raw['completed_at'])
        if timezone.is_naive(completed_at):
            return None
        return Sale(reference, context, attempt, raw['payment_method'], total, paid,
                    change, completed_at, tuple(items))
    except (CartError, KeyError, TypeError, ValueError, InvalidOperation):
        return None


def complete_payment(session, method, token, raw_cash=''):
    """Validate trusted totals and publish one complete, JSON-safe active snapshot.

    Serial retries reuse the receipt. A stable attempt gives the same reference to
    simultaneous retries, but signed cookies cannot enforce a global transaction
    lock or revoke a copied earlier cookie. This app only simulates payments.
    """
    state = cart_state(session)
    payload = unsigned(PAYMENT_SIGNER, token)
    context = uuid_value(state.get('customer_context'))
    attempt = uuid_value(state.get('payment_attempt'))
    if (method not in METHODS or payload.get('method') != method
            or payload.get('attempt') != attempt
            or payload.get('facts') != state.get('reviewed_order')
            or not isinstance(payload.get('facts'), dict)
            or payload['facts'].get('customer_context') != context):
        raise CartError('This payment belongs to an older order. Review your current order again.')
    sale = owned_sale(state)
    if sale:
        if sale.payment_method != method:
            raise CartError('This payment attempt has already been completed with another method.')
        return sale
    _, order, current = payment_order(session)
    if payload['facts'] != current['facts']:
        raise CartError('Your order changed. Review it again before paying.')
    paid = cash_value(raw_cash, order['total']) if method == 'cash' else order['total']
    snapshot = {
        'reference': 'CT-' + UUID(attempt).hex,
        'customer_context': context, 'payment_attempt': attempt, 'payment_method': method,
        'total': format(order['total'], '.2f'), 'amount_paid': format(paid, '.2f'),
        'change': format(paid - order['total'], '.2f'),
        'completed_at': timezone.now().isoformat(),
        'items': [{'product_name': line['product'].name,
                   'unit_price': format(line['unit_price'], '.2f'),
                   'quantity': line['quantity'], 'subtotal': format(line['subtotal'], '.2f')}
                  for line in order['lines']],
    }
    updated = {**state, 'receipt': snapshot, 'active_reference': snapshot['reference']}
    sale = owned_sale(updated)
    if sale is None:
        raise CartError('Receipt could not be validated. Please review your order again.')
    session['kiosk'] = updated
    return sale


def reset_customer(session, token):
    state = cart_state(session)
    sale = owned_sale(state)
    if not sale or unsigned(RESET_SIGNER, token) != {
            'reference': sale.reference, 'context': str(sale.customer_context)}:
        raise CartError('That transaction is no longer active. Your current order was kept.')
    # Replace this browser's active state. Copied older signed cookies cannot be revoked.
    session.cycle_key()
    session['kiosk'] = {'cart': {}, 'revision': 0, 'customer_context': str(uuid4())}
