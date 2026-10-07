"""JSON-safe session quantities and one trusted Decimal order calculation."""

from decimal import Decimal
import re
from uuid import UUID, uuid4

from .models import MAX_AMOUNT, MAX_QUANTITY, Product


class CartError(ValueError):
    pass


def product_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]{0,18}', value):
        raise CartError('Please choose a valid product.')
    result = int(value)
    if result > 2**63 - 1:
        raise CartError('Please choose a valid product.')
    return result


def cart_state(session):
    state = session.get('kiosk', {})
    return state if isinstance(state, dict) else {'cart': None}


def calculate_order(raw_cart):
    """Read only: exclude damaged/unavailable entries, report any required repair."""
    quantities = {}
    needs_refresh = not isinstance(raw_cart, dict)
    for key, quantity in (raw_cart.items() if isinstance(raw_cart, dict) else []):
        try:
            identifier = product_id(key)
        except CartError:
            needs_refresh = True
            continue
        if type(quantity) is not int or not 1 <= quantity <= MAX_QUANTITY:
            needs_refresh = True
            continue
        quantities[identifier] = quantity
    products = Product.objects.filter(pk__in=quantities, is_available=True)
    lines, clean_cart = [], {}
    total = Decimal('0.00')
    for product in products:
        quantity = quantities[product.pk]
        subtotal = product.price * quantity
        lines.append({'product': product, 'quantity': quantity,
                      'unit_price': product.price, 'subtotal': subtotal})
        clean_cart[str(product.pk)] = quantity
        total += subtotal
    needs_refresh |= len(clean_cart) != len(quantities)
    return {'lines': lines, 'cart': clean_cart, 'total': total,
            'item_count': sum(clean_cart.values()), 'needs_refresh': needs_refresh,
            'over_limit': total > MAX_AMOUNT}


def change_cart(session, action, identifier=None):
    """Apply only explicit POST actions. Never accept browser money or quantities."""
    if action not in {'add', 'increase', 'decrease', 'remove', 'refresh'}:
        raise CartError('That order action is not supported.')
    state = cart_state(session)
    order = calculate_order(state.get('cart', {}))
    cart = order['cart'].copy()
    if action == 'refresh':
        if not order['needs_refresh']:
            raise CartError('Your order is already up to date.')
        feedback = 'Order updated. Unavailable or invalid items were removed.'
    else:
        key = str(product_id(identifier))
        product = Product.objects.filter(pk=int(key), is_available=True).first()
        if product is None:
            raise CartError('This item is no longer available. Update your order.')
        quantity = cart.get(key, 0)
        if action != 'add' and quantity == 0:
            raise CartError('This item is not in your order.')
        if action in {'add', 'increase'}:
            if quantity >= MAX_QUANTITY:
                raise CartError(f'You can order up to {MAX_QUANTITY} of each item.')
            cart[key] = quantity + 1
            feedback = f'{product.name} added. Quantity: {quantity + 1}.'
        elif action == 'decrease' and quantity > 1:
            cart[key] = quantity - 1
            feedback = f'{product.name} quantity: {quantity - 1}.'
        else:
            del cart[key]
            feedback = f'{product.name} removed from your order.'
        if order['needs_refresh']:
            feedback += ' Unavailable or invalid items were also removed.'
    new_order = calculate_order(cart)
    if new_order['over_limit'] and action in {'add', 'increase'}:
        raise CartError('This order exceeds the supported total. Remove an item first.')
    try:
        context = str(UUID(str(state.get('customer_context', ''))))
    except ValueError:
        context = str(uuid4())
    revision = state.get('revision', 0)
    revision = revision if type(revision) is int and revision >= 0 else 0
    state = state.copy()
    for key in ('reviewed_order', 'payment_attempt', 'payment_method', 'cash_amount'):
        state.pop(key, None)
    state.update(cart=cart, customer_context=context, revision=revision + 1)
    session['kiosk'] = state
    return feedback
