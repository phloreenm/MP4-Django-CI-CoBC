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

# Constants
CART_VIEW_URL = 'cart:view_cart'

def _build_form_data(request):
    """Extract form data from POST request."""
    return {
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

def _process_cart_item(request, cart, item_id, item_data, order):
    """Process a single cart item and create order line items."""
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
            return False
        
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
        return True
        
    except Product.DoesNotExist:
        messages.error(request, (
            "One of the products in your cart wasn't found in our database. "
            "Please call us for assistance!"
        ))
        order.delete()
        return False

def _get_default_form_data(request):
    """Get default form data based on user authentication status."""
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile:
            return {
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
            return {
                'full_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'comments': '',
            }
    else:
        return {
            'full_name': 'Anonymous User',
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

def checkout(request):
    """Render the checkout page and process the order form."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

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

    if request.method == 'POST':
        return _handle_checkout_post(request, cart)
    else:
        return _handle_checkout_get(request, stripe_public_key, intent, current_cart)

def _handle_checkout_post(request, cart):
    """Handle POST request for checkout form submission."""
    form_data = _build_form_data(request)
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

        # Process each cart item
        if not _process_all_cart_items(request, cart, order):
            return redirect(reverse(CART_VIEW_URL))

        _finalize_order(request, order)
        return redirect(reverse('checkout:success', args=[order.order_number]))
    else:
        messages.error(request, "There was an error with your form. Please double-check your information.")
        return redirect(reverse('checkout:checkout'))

def _handle_checkout_get(request, stripe_public_key, intent, current_cart):
    """Handle GET request for checkout page."""
    default_data = _get_default_form_data(request)
    order_form = OrderForm(initial=default_data)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'cart_items': current_cart.get('cart_items'),
        'total_cost': current_cart.get('cart_total'),
    }
    return render(request, 'checkout/checkout.html', context)

def _process_all_cart_items(request, cart, order):
    """Process all items in the cart and create order line items."""
    for item_id, item_data in cart.items():
        if not _process_cart_item(request, cart, item_id, item_data, order):
            return False
    return True

def _finalize_order(request, order):
    """Finalize the order by calculating totals and sending confirmation email."""
    from orders.emails import send_order_confirmation_email

    # Calculate the order total from the line items.
    total = sum(item.lineitem_total for item in order.lineitems.all())
    order.order_total = total
    # Assume grand_total includes delivery cost.
    order.grand_total = total + order.delivery_cost
    order.save()

    request.session['save_info'] = 'save-info' in request.POST
    
    # Try to send confirmation email, but don't fail the order if email fails
    try:
        send_order_confirmation_email(order)
        messages.info(request, f"Order confirmation email sent to {order.email}")
    except Exception:
        # Log the error but don't break the checkout process
        messages.warning(request, "Order created successfully, but we couldn't send the confirmation email.")


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
    return redirect(reverse(CART_VIEW_URL))