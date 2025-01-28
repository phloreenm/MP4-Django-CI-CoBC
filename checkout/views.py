from django.conf import settings
from django.shortcuts import render
import stripe
from django.http import JsonResponse
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """Displays the Checkout page with cart summary."""
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

def create_checkout_session(request):
    """Creates a Stripe payment session."""
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    cart = request.session.get('cart', {})
    print("Using Stripe Keys:", settings.STRIPE_PUBLIC_KEY)  # Debugging
    print("Using Stripe Keys:", settings.STRIPE_SECRET_KEY)  # Debugging
    if not cart:
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    line_items = []
    for item_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=item_id)
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.name},
                    'unit_amount': int(product.price * 100),  # Convert price to cents
                },
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with ID {item_id} does not exist.'}, status=400)

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

def success(request):
    """Displays the success page after a successful payment."""
    return render(request, 'checkout/success.html')

def cancel(request):
    """Displays the cancellation page if the payment is canceled."""
    return render(request, 'checkout/cancel.html')