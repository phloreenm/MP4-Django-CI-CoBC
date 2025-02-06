from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from orders.models import Order, OrderLineItem
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
            'comments': request.POST.get('comments'),
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # If the user is authenticated, assign the order to the user.
            if request.user.is_authenticated:
                order.user = request.user
            # Extract PaymentIntent ID from client_secret sent via hidden input.
            pid = request.POST.get('client_secret', '').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            # Process each cart item: check stock, create order line items, update stock.
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    # Determine the quantity being purchased.
                    if isinstance(item_data, int):
                        quantity = item_data
                    else:
                        quantity = sum(item_data.get('items_by_size', {}).values())
                    
                    # Check that there is enough stock.
                    if product.stock < quantity:
                        messages.error(request, f"Not enough stock for {product.name}. Available: {product.stock}")
                        order.delete()
                        return redirect(reverse('cart:view_cart'))
                    
                    # Create the OrderLineItem(s).
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                    else:
                        for size, qty in item_data.get('items_by_size', {}).items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=qty,
                                product_size=size,
                            )
                    
                    # Deduct the purchased quantity from stock and save the product.
                    product.stock -= quantity
                    product.save()
                    
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('cart:view_cart'))
            
            from orders.emails import send_order_confirmation_email

            # Calculate the order total from the line items.
            total = sum(item.lineitem_total for item in order.lineitems.all())
            order.order_total = total
            # Assume grand_total includes delivery cost.
            order.grand_total = total + order.delivery_cost
            order.save()

            request.session['save_info'] = 'save-info' in request.POST

            send_order_confirmation_email(order)
            # Redirect to success page with order_number as argument.
            return redirect(reverse('checkout:success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        # GET request: Check for a cart and create a PaymentIntent.
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
        # Prepopulate the form if user is logged in.
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                default_data = {
                    'full_name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'phone_number': profile.phone_number or '',
                    'country': profile.country.code if profile.country else '',
                    'postcode': profile.postcode or '',
                    'town_or_city': profile.city or '',
                    'street_address1': profile.street_address or '',
                    'street_address2': '',
                    'county': profile.county or '',
                    'comments': '',
                }
            else:
                default_data = {
                    'full_name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'comments': '',
                }
        else:
            default_data = {
                'full_name': 'Anonimous User',
                'email': 'phlopping@yahoo.com',
                'phone_number': '07777777777',
                'country': 'GB',
                'postcode': 'SP2 7QY',
                'town_or_city': 'Salisbury',
                'street_address1': '67 Fisherton Street',
                'street_address2': 'CC CAFE',
                'county': 'Wiltshire',
                'comments': 'This is just a comment meant for testing purposes.',
            }
        order_form = OrderForm(initial=default_data)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'cart_items': current_cart.get('cart_items'),
        'total_cost': current_cart.get('cart_total'),
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