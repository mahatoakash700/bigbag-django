from cart.models import Cart, CartItem
from .views import _cart_id


def cart_count(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            count += cart_items.count()
        except Cart.DoesNotExist:
            count = 0
    return dict(count=count)
