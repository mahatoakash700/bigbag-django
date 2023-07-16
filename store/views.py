from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .helpers import pagination
from django.conf import settings

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    if (category_slug != None):
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by(
            'id')  # using order by to avoid warning thrown in terminal
        product_count = products.count()

    # pagination
    # paginator = Paginator(products, no_of_products_per_page)
    # page = request.GET.get('page')
    # paged_products = paginator.get_page(page)

    paged_products = pagination(request,
                                products=products, no_of_products_per_page=settings.PRODUCTS_PER_PAGE)

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        selected_sizes = list(product.sizes.values_list('name', flat=True))
        print('selected_sizes:', selected_sizes)
        selected_colors = list(product.colors.values_list('name', flat=True))
        print('selected_colors:', selected_colors)

        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    checked_color_index = len(selected_colors) - 1
    checked_size_index = len(selected_sizes) - 1

    print("color index: ", checked_color_index)
    print("size index: ", checked_size_index)

    context = {
        'product': product,
        'in_cart': in_cart,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'checked_color_index': checked_color_index,
        'checked_size_index': checked_size_index,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    # q = request.GET.get('q')
    # products = None
    # if q:
    #     products = Product.objects.order_by(
    #         '-created_date').filter(Q(description__icontains=q) | Q(product_name__icontains=q))  # Q is used for multiple queries

    # paged_products = pagination(request,
    #                             products=products, no_of_products_per_page=settings.PRODUCTS_PER_PAGE)
    # context = {
    #     'products': paged_products,
    #     'search_query': q,
    # }

    q = request.GET.get('q')
    products = None
    paged_products = None
    product_count = 0

    if q:
        products = Product.objects.order_by('-created_date').filter(
            Q(description__icontains=q) | Q(product_name__icontains=q))
        product_count = products.count()

        if products:
            paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
            page_number = request.GET.get('page')
            paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
        'search_query': q,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
