from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(f"Adding product: {product.name}, Stock: {product.stock}")

    cart, created = Cart.objects.get_or_create(user=request.user)
    print(f"Cart created: {created}, User: {request.user}")

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    print(f"Cart item created: {created}, Quantity before: {cart_item.quantity}")

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            print(f"Updated quantity: {cart_item.quantity}")
        else:
            print("Cannot exceed available stock.")
            return JsonResponse({"error": "Cannot exceed available stock."}, status=400)
    else:
        cart_item.quantity = 1
        print("New item added with quantity 1.")

    cart_item.save()
    return redirect('cart_view')


# @login_required
# def view_cart(request):
#     """Displays the user's shopping cart."""
#     cart = Cart.objects.filter(user=request.user).first()  # Retrieve the user's cart
#     total_cost = 0
#     items_with_totals = []

#     if cart:
#         for item in cart.items.all():
#             item_total = item.quantity * item.product.price
#             total_cost += item_total
#             items_with_totals.append({
#                 'id': item.id,
#                 'product_name': item.product.name,
#                 'quantity': item.quantity,
#                 'price': item.product.price,
#                 'total': item_total,
#             })
#             print(f"Product in cart: {item.product.name}, Quantity: {item.quantity}, Price: {item.product.price} , Item Total: {item_total}")

#     return render(request, 'cart/cart_view.html', {'items': items_with_totals, 'total_cost': total_cost})
@login_required
def view_cart(request):
    """Displays the user's shopping cart."""
    cart = Cart.objects.filter(user=request.user).first()  # Retrieve the user's cart
    total_cost = 0

    if cart:
        print(f"Cart contains: {cart.items.all()}")
  
        for item in cart.items.all():
            item.total = item.quantity * item.product.price  # Calculează totalul pentru fiecare produs
            total_cost += item.total  # Adaugă la totalul coșului
            print(f"Product in cart: {item.product.name}, Quantity: {item.quantity}, Price: {item.product.price} , Item Total: {item.total}")

    return render(request, 'cart/cart_view.html', {'cart': cart, 'item.total': item.total, 'total_cost': total_cost})


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

        # Validate against available stock
        if new_quantity > cart_item.product.stock:
            new_quantity = cart_item.product.stock  # Cap at available stock

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is 0 or less

        # Recalculate totals
        cart_total = sum(item.quantity * item.product.price for item in cart_item.cart.items.all())
        item_total = cart_item.quantity * cart_item.product.price if cart_item.id else 0

        return JsonResponse({
            "item_quantity": cart_item.quantity,
            "item_total": float(item_total),
            "cart_total": float(cart_total),
        })

    return JsonResponse({"error": "Unauthorized"}, status=403)