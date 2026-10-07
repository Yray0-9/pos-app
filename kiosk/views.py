from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .cart import CartError, calculate_order, cart_state, change_cart
from .models import MAX_QUANTITY, Product


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
    return {'catalog': catalog, 'order': order, 'feedback': feedback, 'current_step': 1}


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
