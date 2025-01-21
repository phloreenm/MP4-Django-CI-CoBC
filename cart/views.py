from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    print("View add_to_cart function")
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')


@login_required
def view_cart(request):
    """Displays the user's shopping cart."""
    cart = Cart.objects.filter(user=request.user).first()  # Retrieve the user's cart
    return render(request, 'cart/cart_view.html', {'cart': cart})
