from uuid import UUID

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .cart import CartError, calculate_order, cart_state, change_cart
from .models import MAX_QUANTITY, Product
from .review import REVIEW_SIGNER, confirm_review, review_facts


ART = {'rice-bowl': ('bowl', 'meal'), 'chicken-wrap': ('wrap', 'warm'),
       'cucumber-lemonade': ('drink', 'fresh'), 'banana-muffin': ('muffin', 'soft'),
       'cheese-bun': ('bun', 'warm'), 'granola-pack': ('granola', 'meal')}


def workspace_context(request, feedback=None):
    order = calculate_order(cart_state(request.session).get('cart', {}))
    catalog = []
    for product in Product.objects.filter(is_available=True):
        art, tone = ART.get(product.seed_key, ('granola', 'meal'))
        quantity = order['cart'].get(str(product.pk), 0)
        catalog.append({'product': product, 'art': art, 'tone': tone,
                        'quantity': quantity, 'at_limit': quantity >= MAX_QUANTITY})
    return {'catalog': catalog, 'order': order, 'feedback': feedback, 'current_step': 1,
            'can_review': bool(order['lines']) and not order['needs_refresh'] and not order['over_limit']}


@never_cache
@require_GET
def home(request):
    return render(request, 'kiosk/home.html', workspace_context(request))


@never_cache
@require_POST
def cart_action(request):
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


def current_order(request):
    state = cart_state(request.session)
    return state, calculate_order(state.get('cart', {}))


@never_cache
@require_GET
def review_order(request):
    state, order = current_order(request)
    token, error = None, None
    try:
        token = REVIEW_SIGNER.sign_object(review_facts(state, order))
    except CartError as problem:
        error = str(problem)
    return render(request, 'kiosk/review.html', {
        'order': order, 'review_token': token, 'review_error': error,
        'current_step': 2, 'header_status': 'Review your order',
    })


@never_cache
@require_POST
def continue_to_payment(request):
    _, order = current_order(request)
    try:
        confirm_review(request.session, order, request.POST.get('review_token', ''))
    except CartError as error:
        messages.error(request, str(error))
        return redirect('kiosk:review')
    return redirect('kiosk:payment')


@never_cache
@require_GET
def payment_entry(request):
    state, order = current_order(request)
    try:
        facts = review_facts(state, order)
        if state.get('reviewed_order') != facts or not state.get('payment_attempt'):
            raise CartError('Please review your current order before continuing to payment.')
        try:
            UUID(str(state['payment_attempt']))
        except ValueError:
            raise CartError('Please review your current order before continuing to payment.') from None
    except CartError as error:
        messages.error(request, str(error))
        return redirect('kiosk:review')
    return render(request, 'kiosk/payment_entry.html', {
        'order': order, 'current_step': 3, 'header_status': 'Your order is ready',
    })
