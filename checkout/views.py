from django.conf import settings
from django.shortcuts import render
import stripe
from django.http import JsonResponse
from products.models import Product

def checkout(request):
    """Afișează pagina de Checkout."""
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout/checkout.html', context)


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    """Creează o sesiune de plată Stripe."""
    YOUR_DOMAIN = "http://127.0.0.1:8000"  # Domeniul local
    cart = request.session.get('cart', {})

    line_items = []
    for item_id, quantity in cart.items():
        product = Product.objects.get(id=item_id)
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price * 100),  # Stripe folosește cenți
            },
            'quantity': quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/checkout/success/',
            cancel_url=YOUR_DOMAIN + '/checkout/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def checkout(request):
    """Afișează pagina de Checkout."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_cost = 0

    for item_id, quantity in cart.items():
        product = Product.objects.get(id=item_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity,
        })
        total_cost += product.price * quantity

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout/checkout.html', context)