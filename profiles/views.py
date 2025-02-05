from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from orders.models import Order
from products.models import Product

@login_required
def my_profile(request):
    profile = request.user.profile

    # Get orders for the user that are approved (or delivered)
    orders = Order.objects.filter(user=request.user, status__iexact='approved')
    # Gather all unique products from these orders that have a digital file available
    downloads = Product.objects.filter(
        orderlineitem__order__in=orders,
        digital_file__isnull=False
    ).distinct()

    context = {
        'profile': profile,
        'downloads': downloads,
    }
    return render(request, 'profiles/my_profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profiles:my_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})