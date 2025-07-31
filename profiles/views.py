from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from orders.models import Order
from products.models import Product


@login_required
def my_profile(request):
    profile = request.user.profile
    # Get orders for the user that are approved or delivered.
    user_orders = request.user.order_set.filter(status__in=['approved', 'delivered'])
    # Build a dictionary of downloadable products.
    downloads_dict = {}
    for order in user_orders:
        for item in order.lineitems.all():
            if item.product.digital_file:
                # If the product is already added, keep the one with the latest order date.
                if (item.product.id not in downloads_dict or
                    order.date > downloads_dict[item.product.id]['order_date']):
                    downloads_dict[item.product.id] = {
                        'product': item.product,
                        'order_number': order.order_number,
                        'order_date': order.date,
                    }
    downloads = list(downloads_dict.values())
    return render(request, 'profiles/my_profile.html', {'profile': profile, 'downloads': downloads})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profiles:my_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'profiles/edit_profile.html', {'form': form})