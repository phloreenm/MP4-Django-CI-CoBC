from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

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
    total_cost = 0

    if cart:
        # Calculate the total cost
        total_cost = sum(item.quantity * item.product.price for item in cart.items.all())

    return render(request, 'cart/cart_view.html', {'cart': cart, 'total_cost': total_cost})


def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()

        # Recalculate the cart total
        cart_total = sum(item.quantity * item.product.price for item in cart_item.cart.items.all())

        # If the request is AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"cart_total": cart_total})

        # Otherwise, redirect to the cart page
        return redirect('cart_view')

    return JsonResponse({"error": "Unauthorized"}, status=403)


def update_cart_quantity(request, item_id):
    """Update the quantity of a cart item."""
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user == request.user:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()

        # Recalculate totals
        cart_total = sum(item.quantity * item.product.price for item in cart_item.cart.items.all())
        item_total = cart_item.quantity * cart_item.product.price if cart_item.id else 0

        return JsonResponse({
            "item_quantity": cart_item.quantity,
            "item_total": float(item_total),  # Ensure numeric type
            "cart_total": float(cart_total),  # Ensure numeric type
        })

    return JsonResponse({"error": "Unauthorized"}, status=403)