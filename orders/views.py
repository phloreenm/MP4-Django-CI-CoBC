from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm, OrderLookupForm

@login_required
def my_orders(request):
    """Display orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    # Allow admin or seller to view any order; regular users see only their own.
    if request.user.is_staff or request.user.groups.filter(name="seller").exists():
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_number):
    """Allow the user to cancel an order if it is still pending."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status not in ['delivered', 'canceled']:
        order.status = 'canceled'
        order.save()
        messages.success(request, "Your order has been canceled.")
    else:
        messages.error(request, "This order cannot be canceled.")
    return redirect('orders:my_orders')

@login_required
def orders_summary(request):
    """
    Displays orders differently based on the user role:
      - Admin (request.user.is_staff) or Seller (user in group 'seller'): sees all orders.
      - Regular user: sees only their own orders.
    """
    user = request.user
    if user.is_staff or user.groups.filter(name='seller').exists():
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
    if not (request.user.is_staff or request.user.groups.filter(name='seller').exists()):
        messages.error(request, "You do not have permission to edit orders.")
        return redirect('orders:orders_summary')
    messages.info(request, "Edit order functionality is not implemented yet.")
    return redirect('orders:orders_summary')

@login_required
def order_delete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if not (request.user.is_staff or request.user.groups.filter(name='seller').exists()):
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
    Once confirmed, the order status is updated, and an email (to be implemented)
    could be sent with download links.
    """
    # Only allow admin or seller to confirm orders
    if not (request.user.is_staff or request.user.groups.filter(name="seller").exists()):
        messages.error(request, "You do not have permission to confirm orders.")
        return redirect('orders:orders_summary')

    order = get_object_or_404(Order, order_number=order_number)
    if order.status.lower() == 'pending':
        order.status = 'approved'  # or 'delivered' if that is your final status
        order.save()
        # Optionally, trigger an email to the customer here with download links
        messages.success(request, f"Order {order.order_number} has been confirmed.")
    else:
        messages.error(request, "Only pending orders can be confirmed.")
    return redirect('orders:orders_summary')

def order_lookup(request):
    """
    Allows an unauthenticated user to look up an order by order number and email.
    If an order is found but is canceled, an error message is shown.
    """
    if request.method == 'POST':
        form = OrderLookupForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']
            email = form.cleaned_data['email']
            try:
                order = Order.objects.get(order_number=order_number, email=email)
                if order.status.lower() in ['canceled', 'anulata']:
                    messages.error(request, "This order has been canceled and is no longer active.")
                    return render(request, 'orders/order_lookup.html', {'form': form})
                return render(request, 'orders/order_detail.html', {'order': order})
            except Order.DoesNotExist:
                messages.error(request, "No order found matching those details. Please check your inputs.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OrderLookupForm()
    return render(request, 'orders/order_lookup.html', {'form': form})