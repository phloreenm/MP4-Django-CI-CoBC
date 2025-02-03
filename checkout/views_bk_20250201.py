from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.context import cart_summary
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe
import json

import logging

logger = logging.getLogger(__name__)

# Set Stripe secret key globally
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment.")
        return redirect(reverse('products'))

    if request.method == 'POST':
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
            # Extract the PaymentIntent ID from the client secret
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0]
            order.stripe_pid = pid
            # (If you have an 'original_cart' field in your Order model, set it here)
            # order.original_cart = json.dumps(cart)
            order.save()

            # Create order line items
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
                                product_size=size,  # if applicable in your model
                            )
                except Product.DoesNotExist:
                    messages.error(request, "A product in your cart wasn't found in our database.")
                    order.delete()
                    return redirect(reverse('cart:view_cart'))
            
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout:success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        # Default data for GET requests (for testing/demo purposes)
        default_data = {
            'full_name': 'Testing user',
            'email': 'anthimosm@yahoo.com',
            'phone_number': '07777777777',
            'country': 'GB',
            'postcode': 'sp2 7qy',
            'town_or_city': 'Salisbury',
            'street_address1': '67 Fisherton Street',
            'street_address2': '',
            'county': 'Wiltshire',
        }
        order_form = OrderForm(initial=default_data)

    # Create a PaymentIntent for the amount
    current_cart = cart_summary(request)
    total = current_cart.get('cart_total', 0)
    stripe_total = round(total * 100)
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)

# def checkout(request):
#     """Render the checkout page and process the order form."""
#     stripe_public_key = settings.STRIPE_PUBLIC_KEY
#     stripe_secret_key = settings.STRIPE_SECRET_KEY

#     if request.method == 'POST':
#         cart = request.session.get('cart', {})
#         if not cart:
#             messages.error(request, "There's nothing in your cart at the moment.")
#             return redirect(reverse('products'))

#         form_data = {
#             'full_name': request.POST['full_name'],
#             'email': request.POST['email'],
#             'phone_number': request.POST['phone_number'],
#             'country': request.POST['country'],
#             'postcode': request.POST['postcode'],
#             'town_or_city': request.POST['town_or_city'],
#             'street_address1': request.POST['street_address1'],
#             'street_address2': request.POST['street_address2'],
#             'county': request.POST['county'],
#         }
#         order_form = OrderForm(form_data)
#         if order_form.is_valid():
#             order = order_form.save(commit=False)
#             pid = request.POST.get('client_secret').split('_secret')[0]
#             order.stripe_pid = pid
#             order.original_cart = json.dumps(cart)
#             order.save()

#             # Add line items to the order
#             for item_id, item_data in cart.items():
#                 try:
#                     product = Product.objects.get(id=item_id)
#                     if isinstance(item_data, int):
#                         line_item = OrderLineItem(
#                             order=order,
#                             product=product,
#                             quantity=item_data,
#                         )
#                         line_item.save()
#                     else:
#                         for size, quantity in item_data['items_by_size'].items():
#                             line_item = OrderLineItem(
#                                 order=order,
#                                 product=product,
#                                 quantity=quantity,
#                                 product_size=size,
#                             )
#                             line_item.save()
#                 except Product.DoesNotExist:
#                     messages.error(request, (
#                         "One of the products in your cart wasn't found in our database."
#                         " Please call us for assistance!")
#                     )
#                     order.delete()
#                     return redirect(reverse('cart:view_cart'))

#             # Redirect to success page
#             request.session['save_info'] = 'save-info' in request.POST
#             return redirect(reverse('checkout:success', args=[order.order_number]))
#         else:
#             messages.error(request, 'There was an error with your form. Please double-check your information.')
#     else:
#         cart = request.session.get('cart', {})
#         if not cart:
#             messages.error(request, "There's nothing in your cart at the moment.")
#             return redirect(reverse('products'))

#         current_cart = cart_summary(request)
#         total = current_cart['cart_total']
#         stripe_total = round(total * 100)
#         intent = stripe.PaymentIntent.create(
#             amount=stripe_total,
#             currency=settings.STRIPE_CURRENCY,
#         )

#         order_form = OrderForm()

#     context = {
#         'order_form': order_form,
#         'stripe_public_key': stripe_public_key,
#         'client_secret': intent.client_secret,
#     }
#     return render(request, 'checkout/checkout.html', context)

def send_order_confirmation_email(order):
    """Send an email confirmation to the customer"""
    subject = render_to_string("checkout/confirmation_emails/confirmation_email_subject.txt", {"order": order})
    body = render_to_string("checkout/confirmation_emails/confirmation_email_body.txt", {"order": order})

    send_mail(
        subject.strip(),
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

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
        try:
            cart = request.session.get('cart', {})
            if not cart:
                return JsonResponse({'error': 'Your cart is empty.'}, status=400)
            # ✅ Log incoming data for debugging
            print("Request POST data:", request.POST)
            # ✅ Retrieve the latest order associated with the session (by stripe_pid)
            pid = request.POST.get('client_secret', '').split('_secret')[0]
            if not pid:
                return JsonResponse({'error': 'No Stripe Payment Intent found.'}, status=400)
            print(f"Extracted Payment Intent ID: {pid}")
            order = Order.objects.filter(stripe_pid=pid).order_by('-date').first()
            if not order:
                return JsonResponse({'error': 'No order found matching this payment intent.'}, status=400)
            print(f"Processing payment for order: {order.order_number}")

            return JsonResponse({'success': True, 'redirect_url': reverse('checkout:success', args=[order.order_number])})

        except Exception as e:
            print(f"Payment processing error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request.'}, status=400)

def success(request, order_number):
    """Display the success page and send a confirmation email."""
    order = get_object_or_404(Order, order_number=order_number)  # ✅ Ensure order exists

    # Send confirmation email
    send_order_confirmation_email(order)

    # Clear the cart after successful payment
    if 'cart' in request.session:
        del request.session['cart']

    messages.success(request, f"Your payment was successful. Order #{order_number} has been processed!")
    return render(request, 'checkout/success.html', {'order': order})


def cancel(request):
    """Handle canceled checkouts."""
    messages.warning(request, "Your payment was canceled. You can retry or return to your cart.")
    return redirect(reverse('cart:view_cart'))