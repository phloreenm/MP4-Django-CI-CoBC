# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm
from .forms import OrderLookupForm


@login_required
def my_orders(request):
    """Display orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    """Display details for a specific order."""
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
      - Admin (request.user.is_staff): sees all orders with full CRUD controls.
      - Seller (user in group 'seller'): sees all orders (or a subset if desired), with full controls.
      - Regular user: sees only their own orders with limited actions (e.g., view, cancel if pending).
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
    # Only admin or seller can edit
    if not (request.user.is_staff or request.user.groups.filter(name='seller').exists()):
        messages.error(request, "You do not have permission to edit orders.")
        return redirect('orders:orders_summary')
    # Implement the edit logic here (e.g., a ModelForm for editing order details)
    # For now, simply render a placeholder
    messages.info(request, "Edit order functionality is not implemented yet.")
    return redirect('orders:orders_summary')

@login_required
def order_delete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if not (request.user.is_staff or request.user.groups.filter(name='seller').exists()):
        messages.error(request, "You do not have permission to delete orders.")
        return redirect('orders:orders_summary')
    # Implement delete logic (e.g., confirm deletion and then delete)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('orders:orders_summary')

@login_required
def order_alter(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status != 'pending':
        messages.error(request, "Only pending orders can be altered.")
        return redirect('orders:my_orders')
    # Implement alter logic (e.g., a form to update order comments or address)
    messages.info(request, "Alter order functionality is not implemented yet.")
    return redirect('orders:my_orders')

def order_lookup(request):
    """
    Allows a user (unauthenticated or otherwise) to look up an order by its order number and email.
    If an order is found but has been canceled, an error message is displayed.
    """
    if request.method == 'POST':
        form = OrderLookupForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']
            email = form.cleaned_data['email']
            try:
                order = Order.objects.get(order_number=order_number, email=email)
                # Check if the order is canceled. Adjust the condition if needed.
                if order.status.lower() in ['canceled', 'anulata']:
                    messages.error(request, "This order has been canceled and is no longer active.")
                    return render(request, 'orders/order_lookup.html', {'form': form})
                # Order found and active: render its detail page.
                return render(request, 'orders/order_detail.html', {'order': order})
            except Order.DoesNotExist:
                messages.error(request, "No order found matching those details. Please check your inputs.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OrderLookupForm()
    return render(request, 'orders/order_lookup.html', {'form': form})