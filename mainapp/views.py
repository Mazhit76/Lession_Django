from django.shortcuts import render
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    title = 'Главная'
    products = Product.objects.all()

    content = {
        'slides': [
            {'path_photo': 'vendor/img/slides/slide-1.jpg',
                'alt_text': 'First slide'},
            {'path_photo': 'vendor/img/slides/slide-2.jpg',
                'alt_text': 'Second slide'},
            {'path_photo': 'vendor/img/slides/slide-3.jpg',
                'alt_text': 'Third slide'},
        ],
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


# def products(request, id=None):  # pk-это то что выделено в shop/urls.py include()
#     # title = 'Главная'
#     # products = Product.objects.all()
#     print(id)  # Это мы выводим на экран терминала номер страницы которую набрали  передано в mainapp/urls.py
#     content = {
#         'title': 'GeekShop - Категории',
#         'categories': ProductCategory.objects.all(),
#         'products': Product.objects.all(),
#     }
#     return render(request, 'mainapp/products.html', content)

def products(request, category_id=None, page=1):
    """Without pagination."""
    context = {'title': 'GeekShop - Категории',
               'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(
            category_id=category_id).order_by('price')
        # order_by-сортировка вывода по price
    else:
        products = Product.objects.all().order_by('price')
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)


def __str__(self):
    return self.username
