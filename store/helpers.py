from django.core.paginator import Paginator


def pagination(request, products, no_of_products_per_page):
    paginator = Paginator(products, no_of_products_per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)
