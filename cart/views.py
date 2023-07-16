from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.


def _cart_id(request):
    id = request.session.session_key
    if not id:
        id = request.session.create()
    return id


def add_to_cart(request, product_id):
    selected_color = request.POST.get('color')
    selected_size = request.POST.get('size')
    if selected_color and selected_size is not None:
        selected_color = selected_color.capitalize()
        selected_size = selected_size.upper()

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_items = CartItem.objects.filter(cart=cart)

    if selected_color and selected_size:
        for cart_item in cart_items:
            if (
                cart_item.product == product and
                cart_item.size == selected_size and
                cart_item.color == selected_color
            ):
                cart_item.quantity += 1
                cart_item.save()
                return redirect('cart')

    else:
        has_size_and_color = False
        for size in product.sizes.all():
            for color in product.colors.all():
                if size and color:
                    has_size_and_color = True
                    break
            if has_size_and_color:
                break

        if not has_size_and_color:
            for cart_item in cart_items:
                if cart_item.product == product:
                    cart_item.quantity += 1
                    cart_item.save()
                    return redirect('cart')

    cart_item = CartItem.objects.create(
        product=product,
        cart=cart,
        quantity=1,
        color=selected_color,
        size=selected_size
    )

    return redirect('cart')


def remove_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id) Also works
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        if (cart_item.quantity > 1):
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        final_amount = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            final_amount = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'quantity': quantity,
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
        'final_amount': final_amount,
    }
    return render(request, 'store/cart.html', context)

# Explanation
# 1. first from prduct_detail.html product is is passed whuch enters into add_to_cart function
# 2. Using the product id, product is captured from db
# 3. Now cart id captured from browser session and is then saved into cart table in db(At first cart table is empty)
# 4. Similarly cart item is captured by passing product and cart value in parameter(cart item table too is empty in db)
# 5. Now in cart function, cart object is captured by passing cart session id from browser
# 6. cart item object is captured by passing the cart value created in above step
# 7. From cart_items, iterate and capture the total amount and quantity and pass it to html through context
