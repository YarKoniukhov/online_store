from django.shortcuts import render,  get_object_or_404
from .models import Category, Brand, Product, Size
from django.db.models import Q


def index(request):
    return render(request, 'shop/index.html', {})


def product_list(request, category_slug=None, brand_slug=None):
    category = None
    brand = None

    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True).order_by('-created')

    sizes = Size.objects.all().order_by('id')
    selected_sizes = request.GET.getlist('size')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if brand_slug:
        brand = get_object_or_404(Brand, slug_brand=brand_slug)
        products = products.filter(brand=brand)

    if 'size' in request.GET:
        selected_sizes = request.GET.getlist('size')
        if 'all' not in selected_sizes:
            products = products.filter(sizes__slug_size__in=selected_sizes)

    context = {
        'category': category,
        'brand': brand,

        'categories': categories,
        'brands': brands,
        'products': products,

        'sizes': sizes,
        'selected_sizes': selected_sizes,
    }

    return render(request, 'shop/product/shop.html', context)







"""

def product_list_by_size(request):
    sizes = request.GET.getlist('size')  # Получаем выбранные размеры
    products = Product.objects.filter(size__in=sizes)  # Фильтруем товары по размерам
    context = {
        'products': products
    }
    return render(request, 'shop/product_list.html', context)



def product_list(request):
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all().order_by('-created')

    category = None  # Устанавливаем значение по умолчанию
    brand = None  # Устанавливаем значение по умолчанию

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if brand_slug:
        brand = get_object_or_404(Brand, slug_brand=brand_slug)
        products = products.filter(brand=brand)

    context = {
        'categories': categories,
        'brands': brands,

        'selected_category': category_slug,
        'selected_brand': brand_slug,

        'category': category,  # Передаем переменную category в контекст
        'brand': brand,  # Передаем переменную brand в контекст

        'products': products,
    }

    return render(request, 'shop/product/shop.html', context)
"""


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})
