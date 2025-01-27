from django.shortcuts import get_object_or_404
from products.models import Product

def cart_summary(request):
    cart = request.session.get('cart', {})
    total = sum(
        get_object_or_404(Product, pk=item_id).price * quantity
        for item_id, quantity in cart.items()
    )
    return {'cart_total': total}