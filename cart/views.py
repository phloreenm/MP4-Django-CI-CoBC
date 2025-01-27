from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def view_cart(request):
    cart = request.session.get('cart', {})
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Adaugă un produs în coș folosind sesiuni."""
    product = get_object_or_404(Product, pk=product_id)  # Verificăm dacă produsul există
    cart = request.session.get('cart', {})  # Preluăm coșul din sesiune sau inițiem unul nou

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Creștem cantitatea produsului dacă există deja
    else:
        cart[str(product_id)] = 1  # Adăugăm produsul cu cantitatea 1

    request.session['cart'] = cart  # Actualizăm sesiunea
    return redirect('cart:view_cart')  # Redirect către pagina coșului

def remove_from_cart(request, product_id):
    """Elimină un produs din coș."""
    cart = request.session.get('cart', {})  # Preluăm coșul din sesiune

    if str(product_id) in cart:
        del cart[str(product_id)]  # Ștergem produsul din coș
        request.session['cart'] = cart  # Actualizăm sesiunea

    return redirect('cart:view_cart') 