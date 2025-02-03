from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
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

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment.")
            return redirect(reverse('products'))

        # Build form data from POST
        form_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'country': request.POST.get('country'),
            'postcode': request.POST.get('postcode'),
            'town_or_city': request.POST.get('town_or_city'),
            'street_address1': request.POST.get('street_address1'),
            'street_address2': request.POST.get('street_address2'),
            'county': request.POST.get('county'),
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # Extract PaymentIntent ID from client_secret sent via hidden input
            pid = request.POST.get('client_secret', '').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            # Add line items to the order
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    else:
                        for size, quantity in item_data.get('items_by_size', {}).items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('cart:view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            # Redirect to success page with order_number as argument
            return redirect(reverse('checkout:success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
            # Fall through to re-render the form with errors.
    else:
        # GET request: Check for a cart and create a PaymentIntent
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

        # Default data for testing/demo purposes in the order form
        default_data = {
            'full_name': 'Testing user',
            'email': 'anthimosm@yahoo.com',
            'phone_number': '07777777777',
            'country': 'GB',
            'postcode': 'SP2 7QY',
            'town_or_city': 'Salisbury',
            'street_address1': '67 Fisherton Street',
            'street_address2': 'CC CAFE',
            'county': 'Wiltshire',
        }
        order_form = OrderForm(initial=default_data)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        # We pass the full client_secret (so that our JavaScript can use it)
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def success(request, order_number):
    """Display the success page with order details."""
    order = get_object_or_404(Order, order_number=order_number)
    # Clear the cart after successful payment
    if 'cart' in request.session:
        del request.session['cart']
    messages.success(request, "Your payment was successful. Thank you for your order!")
    return render(request, 'checkout/success.html', {'order': order})


def cancel(request):
    """Handle canceled checkouts."""
    messages.warning(request, "Your payment was canceled. You can retry or return to your cart.")
    return redirect(reverse('cart:view_cart'))