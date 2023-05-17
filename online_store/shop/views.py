from django.shortcuts import render,  get_object_or_404
from .models import Brand, Category, Product


def index(request):
    return render(request, 'shop/index.html', {})

'''
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug or brand_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/shop.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})'''


def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})


def product_list_by_brand(request, brand_slug):
    brand = get_object_or_404(Brand, slug_brand=brand_slug)
    products = Product.objects.filter(brand=brand)
    return render(request, 'shop/product_list.html', {'brand': brand, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})
