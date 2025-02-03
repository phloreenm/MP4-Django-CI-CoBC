from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.context import cart_summary
import stripe
import json

# Set Stripe secret key globally
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Render the checkout page and process the order form."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment.")
            return redirect(reverse('products'))

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            # Add line items to the order
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database."
                        " Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('cart:view_cart'))

            # Redirect to success page
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout:success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment.")
            return redirect(reverse('products'))

        current_cart = cart_summary(request)
        total = current_cart['cart_total']
        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def create_checkout_session(request):
    """Create a Stripe payment session."""
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    cart = request.session.get('cart', {})
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

def process_payment(request):
    """Process the payment after form submission."""
    if request.method == 'POST':
        # You can add your logic here to process the payment
        return JsonResponse({'success': True, 'redirect_url': reverse('checkout:success')})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if 'cart' in request.session:
        del request.session['cart']
    messages.success(request, "Your payment was successful. Thank you for your order!")
    return render(request, 'checkout/success.html', {'order': order})


def cancel(request):
    """Handle canceled checkouts."""
    messages.warning(request, "Your payment was canceled. You can retry or return to your cart.")
    return redirect(reverse('cart:view_cart'))