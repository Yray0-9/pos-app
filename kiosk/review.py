"""Bind review confirmation to current trusted cart facts, without storing a sale."""

from uuid import UUID, uuid4

from django.core import signing

from .cart import CartError


REVIEW_SIGNER = signing.Signer(salt='kiosk.order-review')


def review_facts(state, order):
    if order['needs_refresh']:
        raise CartError('Some saved items are invalid or unavailable. Go back and update your order before continuing.')
    if not order['lines']:
        raise CartError('Your order is empty. Add an item before continuing.')
    if order['over_limit']:
        raise CartError('Your order exceeds the supported total. Go back and reduce or remove items.')
    try:
        context = str(UUID(str(state.get('customer_context', ''))))
    except ValueError:
        raise CartError('Your order session needs refreshing. Go back and adjust an item, then review again.') from None
    revision = state.get('revision')
    if type(revision) is not int or revision < 1:
        raise CartError('Your order session needs refreshing. Go back and adjust an item, then review again.')
    return {
        'customer_context': context, 'revision': revision,
        'items': [{'product_id': line['product'].pk, 'name': line['product'].name,
                   'unit_price': format(line['unit_price'], '.2f'),
                   'quantity': line['quantity'], 'subtotal': format(line['subtotal'], '.2f')}
                  for line in order['lines']],
        'total': format(order['total'], '.2f'),
    }


def confirm_review(session, order, token):
    state = session.get('kiosk', {})
    # The caller uses cart_state; require the valid namespace again at the write boundary.
    state = state if isinstance(state, dict) else {}
    facts = review_facts(state, order)
    try:
        displayed = REVIEW_SIGNER.unsign_object(token)
    except (signing.BadSignature, ValueError, TypeError):
        raise CartError('Please review your order again before continuing.') from None
    if displayed != facts:
        raise CartError('Your order changed. Please check the updated order and continue again.')
    try:
        attempt = str(UUID(str(state.get('payment_attempt', ''))))
    except ValueError:
        attempt = None
    if state.get('reviewed_order') != facts or attempt is None:
        attempt = str(uuid4())
    updated = state.copy()
    updated.update(reviewed_order=facts, payment_attempt=attempt)
    # Any later method/cash form belongs to the confirmed facts, not an older order.
    if state.get('reviewed_order') != facts:
        updated.pop('payment_method', None)
        updated.pop('cash_amount', None)
    session['kiosk'] = updated
    return facts
