# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm

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