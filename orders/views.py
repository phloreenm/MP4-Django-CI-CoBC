from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Order
from .forms import OrderForm, OrderLookupForm
import os
from django.http import FileResponse, Http404
from products.models import Product
from orders.emails import send_order_approval_email

@login_required
def my_orders(request):
    """Display orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    """
    Display details for a specific order.
    Admins, sellers, or superusers can view any order;
    regular users can only view their own orders.
    """
    if request.user.is_staff or request.user.groups.filter(name="seller").exists():
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_number):
    """Allow the user to cancel an order if it is still pending and restore product stock."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status not in ['delivered', 'canceled']:
        # Restore stock for each order line item.
        for item in order.lineitems.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        # Update order status.
        order.status = 'canceled'
        order.save()
        send_order_cancellation_email(order)
        messages.success(request, "Your order has been canceled.")
    else:
        messages.error(request, "This order cannot be canceled.")
    return redirect('orders:my_orders')

def cancel_order_lookup(request, order_number):
    """
    Allows an unauthenticated (or authenticated) user who has looked up their order
    to cancel it. The view should confirm the cancellation (optionally, you can require
    a confirmation step) and restore the stock for each item in the order.
    """
    # Here, you might pass along the email via GET parameters or have the user confirm it.
    email = request.GET.get('email', None)
    if not email:
        messages.error(request, "Email verification is required to cancel the order.")
        return redirect('orders:order_lookup')
    
    try:
        order = Order.objects.get(order_number=order_number, email=email)
        if order.status.lower() not in ['delivered', 'canceled']:
            # Restore stock for each order line item.
            for item in order.lineitems.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            order.status = 'canceled'
            order.save()
            send_order_cancellation_email(order)
            messages.success(request, "Your order has been canceled and the stock has been updated.")
        else:
            messages.error(request, "This order cannot be canceled.")
    except Order.DoesNotExist:
        messages.error(request, "No order found with the provided details.")
    return redirect('orders:order_lookup')


@login_required
def orders_summary(request):
    """
    Displays orders based on the user's role:
      - Admins, sellers, or superusers see all orders.
      - Regular users see only their own orders.
    """
    user = request.user
    if user.is_staff or user.groups.filter(name="seller").exists():
        orders = Order.objects.all().order_by('-date')
        role = 'admin_or_seller'
    else:
        orders = Order.objects.filter(user=user).order_by('-date')
        role = 'client'
    context = {
        'orders': orders,
        'role': role,
    }
    return render(request, 'orders/orders_summary.html', context)

@login_required
def order_edit(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if not (request.user.is_staff or request.user.groups.filter(name="seller").exists()):
        messages.error(request, "You do not have permission to edit orders.")
        return redirect('orders:orders_summary')
    messages.info(request, "Edit order functionality is not implemented yet.")
    return redirect('orders:orders_summary')

@login_required
def order_delete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if not (request.user.is_staff or request.user.groups.filter(name="seller").exists()):
        messages.error(request, "You do not have permission to delete orders.")
        return redirect('orders:orders_summary')
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('orders:orders_summary')

@login_required
def order_alter(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status != 'pending':
        messages.error(request, "Only pending orders can be altered.")
        return redirect('orders:my_orders')
    messages.info(request, "Alter order functionality is not implemented yet.")
    return redirect('orders:my_orders')

@login_required
def confirm_order(request, order_number):
    """
    Allows an admin or seller to confirm (approve) an order.
    Once confirmed, the order status is updated (to 'approved'),
    and an email notification (to be implemented) could be sent.
    """
    if not (request.user.is_staff or request.user.groups.filter(name="seller").exists()):
        messages.error(request, "You do not have permission to confirm orders.")
        return redirect('orders:orders_summary')
    order = get_object_or_404(Order, order_number=order_number)
    if order.status.lower() == 'pending':
        order.status = 'approved'
        order.save()
        send_order_approval_email(order)
        messages.success(request, f"Order {order.order_number} has been confirmed.")
    else:
        messages.error(request, "Only pending orders can be confirmed.")
    return redirect('orders:orders_summary')

def order_lookup(request):
    """
    Allows an unauthenticated (or authenticated) user to look up an order by its
    order number and email. If an order is found and active, displays order details
    along with a cancel option.
    """
    order = None
    if request.method == 'POST':
        form = OrderLookupForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']
            email = form.cleaned_data['email']
            try:
                order = Order.objects.get(order_number=order_number, email=email)
                if order.status.lower() in ['canceled', 'anulata']:
                    messages.error(request, "This order has been canceled and is no longer active.")
                    order = None  # Do not show order details
                # If order exists and is active just display details.
            except Order.DoesNotExist:
                messages.error(request, "No order found matching those details. Please check your inputs.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OrderLookupForm()
    return render(request, 'orders/order_lookup.html', {'form': form, 'order': order})


def download_product(request, order_number, product_id):
    """
    Serves the digital file for the given product if the order is spproved.
    """
    # Retrieve the order.
    order = get_object_or_404(Order, order_number=order_number)
    # Allow download only if order is approved/delivered.
    if order.status.lower() not in ['approved', 'delivered']:
        raise Http404("This order is not approved for download.")
    # Retrieve the product.
    product = get_object_or_404(Product, id=product_id)
    # Ensure the product has a digital file.
    if not product.digital_file:
        raise Http404("No digital file available for this product.")
    try:
        return FileResponse(product.digital_file.open('rb'), content_type='application/pdf')
    except Exception:
        raise Http404("Error retrieving the file.")

