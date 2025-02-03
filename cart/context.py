from django.shortcuts import get_object_or_404
from products.models import Product

def cart_summary(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })
    return {'cart_total': total, 'cart_items': cart_items}