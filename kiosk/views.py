from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .cart import CartError, calculate_order, cart_state, change_cart
from .catalog import MAX_QUANTITY, available_products
from .checkout import (METHODS, REVIEW_SIGNER, RESET_SIGNER, confirm_order,
                       complete_payment, order_facts, owned_sale, payment_order,
                       payment_token, reset_customer)


ART = {'rice-bowl': ('bowl', 'meal'), 'chicken-wrap': ('wrap', 'warm'),
       'cucumber-lemonade': ('drink', 'fresh'), 'banana-muffin': ('muffin', 'soft'),
       'cheese-bun': ('bun', 'warm'), 'granola-pack': ('granola', 'meal')}


def workspace_context(request, feedback=None):
    order = calculate_order(cart_state(request.session).get('cart', {}))
    catalog = []
    for product in available_products():
        art, tone = ART.get(product.seed_key, ('granola', 'meal'))
        quantity = order['cart'].get(str(product.pk), 0)
        catalog.append({'product': product, 'art': art, 'tone': tone,
                        'quantity': quantity, 'at_limit': quantity >= MAX_QUANTITY})
    return {'catalog': catalog, 'order': order, 'feedback': feedback, 'current_step': 1,
            'can_review': bool(order['lines']) and not order['needs_refresh'] and not order['over_limit']}


@never_cache
@require_GET
def home(request):
    if owned_sale(cart_state(request.session)):
        return redirect('kiosk:receipt')
    return render(request, 'kiosk/home.html', workspace_context(request))


@never_cache
@require_POST
def cart_action(request):
    if owned_sale(cart_state(request.session)):
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'redirect': '/receipt/'}, status=409)
        return redirect('kiosk:receipt')
    try:
        text = change_cart(request.session, request.POST.get('action'),
                           request.POST.get('product_id'))
        kind, status = 'success', 200
    except CartError as error:
        text, kind, status = str(error), 'error', 400
    if request.headers.get('Accept') == 'application/json':
        html = render_to_string('kiosk/components/workspace.html',
                               workspace_context(request, {'text': text, 'kind': kind}),
                               request=request)
        return JsonResponse({'html': html}, status=status)
    getattr(messages, kind)(request, text)
    return redirect('kiosk:home')


@never_cache
@require_GET
def review_order(request):
    state = cart_state(request.session)
    if owned_sale(state):
        return redirect('kiosk:receipt')
    order = calculate_order(state.get('cart', {}))
    token, error = None, None
    try:
        token = REVIEW_SIGNER.sign_object(order_facts(state, order))
    except CartError as problem:
        error = str(problem)
    return render(request, 'kiosk/review.html', {'order': order, 'review_token': token,
                  'review_error': error, 'current_step': 2, 'header_status': 'Review your order'})


@never_cache
@require_POST
def continue_to_payment(request):
    if owned_sale(cart_state(request.session)):
        return redirect('kiosk:receipt')
    try:
        confirm_order(request.session, request.POST.get('review_token', ''))
    except CartError as error:
        messages.error(request, str(error))
        return redirect('kiosk:review')
    return redirect('kiosk:payment')


def payment_context(request, method=None):
    if method is not None:
        order, token = payment_token(request.session, method)
    else:
        _, order, _ = payment_order(request.session)
        token = None
    return {'order': order, 'method': method, 'method_label': METHODS.get(method),
            'payment_token': token, 'current_step': 3, 'header_status': 'Simulated payment',
            'keypad_keys': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0', 'backspace']}


@never_cache
@require_GET
def payment(request, method=None):
    if owned_sale(cart_state(request.session)):
        return redirect('kiosk:success')
    try:
        context = payment_context(request, method)
    except CartError as error:
        messages.error(request, str(error))
        return redirect('kiosk:review')
    return render(request, 'kiosk/payment.html', context)


@never_cache
@require_POST
def pay(request, method):
    try:
        complete_payment(request.session, method, request.POST.get('payment_token', ''),
                         request.POST.get('amount_paid', ''))
    except CartError as error:
        if owned_sale(cart_state(request.session)):
            messages.error(request, str(error))
            return redirect('kiosk:success')
        try:
            context = payment_context(request, method)
        except CartError:
            messages.error(request, str(error))
            return redirect('kiosk:review')
        context.update(payment_error=str(error), cash_input=request.POST.get('amount_paid', '')[:16])
        return render(request, 'kiosk/payment.html', context, status=400)
    return redirect('kiosk:success')


@never_cache
@require_GET
def success(request):
    sale = owned_sale(cart_state(request.session))
    if not sale:
        messages.info(request, 'There is no completed payment for this customer.')
        return redirect('kiosk:home')
    return render(request, 'kiosk/success.html', {'sale': sale, 'current_step': 3,
                                               'header_status': 'Payment complete'})


@never_cache
@require_GET
def receipt(request, reference=None):
    sale = owned_sale(cart_state(request.session))
    if not sale or (reference is not None and reference != sale.reference):
        messages.info(request, 'That receipt is not available for the current customer.')
        return redirect('kiosk:home')
    return render(request, 'kiosk/receipt.html', {'sale': sale, 'current_step': 4,
                  'header_status': 'Your receipt', 'reset_token': RESET_SIGNER.sign_object({
                  'reference': sale.reference, 'context': str(sale.customer_context)})})


@never_cache
@require_POST
def new_transaction(request):
    try:
        reset_customer(request.session, request.POST.get('reset_token', ''))
    except CartError as error:
        messages.error(request, str(error))
        return redirect('kiosk:home')
    # Old feedback is scoped to the previous customer's transaction.
    list(messages.get_messages(request))
    return redirect('kiosk:home')
