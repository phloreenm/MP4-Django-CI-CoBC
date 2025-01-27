from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages

def view_cart(request):
    """Afișează conținutul coșului de cumpărături."""
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

# def view_cart(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total_cost = 0

#     for item_id, quantity in cart.items():
#         product = get_object_or_404(Product, pk=item_id)
        
#         # Validare pentru stoc
#         if quantity > product.stock:
#             messages.warning(request, f"Not enough stock for {product.name}. Only {product.stock} available.")
#             quantity = product.stock
#             cart[str(item_id)] = quantity  # Actualizăm sesiunea

#         total_cost += product.price * quantity
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'total': product.price * quantity,
#         })

    request.session['cart'] = cart  # Salvăm modificările în sesiune
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
    """Adaugă un produs în coș."""
    product = get_object_or_404(Product, pk=product_id)  # Verificăm dacă produsul există
    cart = request.session.get('cart', {})  # Preluăm coșul din sesiune sau inițiem unul nou

    # Adăugăm produsul în coș sau creștem cantitatea
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart  # Salvăm coșul în sesiune
    request.session.modified = True  # Marchem sesiunea ca modificată pentru a salva schimbările
    print("Cart after addition:", request.session['cart'])  # Debugging

    return redirect('cart:view_cart')


def remove_from_cart(request, product_id):
    """Elimină un produs din coș."""
    cart = request.session.get('cart', {})  # Preluăm coșul din sesiune

    if str(product_id) in cart:
        del cart[str(product_id)]  # Ștergem produsul din coș
        request.session['cart'] = cart  # Actualizăm sesiunea

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