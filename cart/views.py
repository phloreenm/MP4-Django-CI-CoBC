from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages
from django.http import JsonResponse

def view_cart(request):
    """Display basket contents"""
    cart = request.session.get('cart', {})
    print("Cart in session:", cart)  # Debugging
    cart_items = []
    total_cost = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total_cost += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity,
        })

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart/cart.html', context)

    request.session['cart'] = cart  # Save the cart in the session
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart/cart.html', context)

    context = {
        'cart': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=product_id)  # Check if the product exists
    cart = request.session.get('cart', {})  # We get the cart from the session

    # Add the product or increase quantity
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart  # Save the cart in the session
    request.session.modified = True  # Mark the session as modified
    print("Cart after addition:", request.session['cart'])  # Debugging only

    # Calculate total cost and total quantity
    total_cost = 0
    total_quantity = 0
    for item_id, quantity in cart.items():
        prod = get_object_or_404(Product, pk=item_id)
        total_cost += prod.price * quantity
        total_quantity += quantity

    # If this is an AJAX request, return JSON instead of redirecting
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = {
            'success': f"{product.name} added to cart",
            'total_cost': float(total_cost),
            'total_quantity': total_quantity,
        }
        return JsonResponse(data)
    else:
        return redirect('cart:view_cart')


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = request.session.get('cart', {})  # Take the cart from the session

    if str(product_id) in cart:
        del cart[str(product_id)]  # Delete the product from the cart
        request.session['cart'] = cart  # Update the cart in the session

    return redirect('cart:view_cart')

def update_quantity(request, product_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, pk=product_id)

        if quantity <= product.stock:
            cart[str(product_id)] = quantity
            messages.success(request, f"Updated {product.name} quantity to {quantity}.")
        else:
            messages.error(request, f"Not enough stock for {product.name}. Only {product.stock} available.")

        request.session['cart'] = cart
    return redirect('cart:view_cart')