from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from .models import Category, Brand, Product
from django.db.models import Q, Min, Max
from random import sample


def index(request):
    return render(request, 'shop/index.html', {})


def product_list(request, category_name):
    # category = Category.objects.get(name=category_name)
    category = get_object_or_404(Category, name=category_name)

    products = Product.objects.filter(category=category)
    subcategories = category.subcategories.all()
    # Получаем бренды, связанные с продуктами из категории "Обличчя"
    brands = Brand.objects.filter(product__category=category).distinct()

    # Получаем выбранные подкатегории из запроса
    selected_subcategories = request.GET.getlist('subcategory')
    all_subcategories_selected = 'all' in request.GET

    selected_brands = request.GET.getlist('brand')
    all_brands_selected = 'all_brands' in request.GET

    if all_subcategories_selected:
        # Если выбраны "Всі категорії", сбросить выбранные подкатегории
        selected_subcategories = [str(subcategory.id) for subcategory in subcategories]

    if all_brands_selected:
        selected_brands = [str(brand.id) for brand in brands]

    # Объединяем фильтры для подкатегорий и брендов
    query = Q()

    # Применяем фильтрацию по подкатегориям
    if selected_subcategories:
        query &= Q(subcategory__id__in=selected_subcategories)
        # products = products.filter(subcategory__id__in=selected_subcategories)

    # Применяем фильтрацию по брендам
    if selected_brands:
        query &= Q(brand__in=selected_brands)
        # products = products.filter(brand__id__in=selected_brands)

    # Получаем параметры цены из GET-запроса
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Фильтрация по цене
    if min_price is not None and max_price is not None:
        try:
            min_price = int(min_price)
            max_price = int(max_price)
        except ValueError:
            pass
        else:
            query &= Q(price__gte=min_price, price__lte=max_price)

    min_price = int(products.aggregate(Min('price'))['price__min'])
    max_price = int(products.aggregate(Max('price'))['price__max'])

    # Применяем фильтр к товарам
    if query:
        products = products.filter(query)

    context = {
        'products': products,
        'category': category,
        'subcategories': subcategories,
        'selected_subcategories': selected_subcategories,  # Передаем выбранные подкатегории в контекст
        'all_subcategories_selected': all_subcategories_selected,
        'brands': brands,  # Передаем список брендов в контекст
        'selected_brands': selected_brands,
        'all_brands_selected': all_brands_selected,
        'min_price': min_price,
        'max_price': max_price,
        'current_view': 'face_list',  # Добавьте имя представления
        'category_name': category_name,
    }

    return render(request, 'shop/product/product_list.html', context)


def product_detail(request, id, url):
    product = get_object_or_404(Product, id=id, url=url, available=True)
    category = product.category  # Получаем категорию продукта

    # cart_product_form = CartAddProductForm()

    # Получите подкатегорию текущего товара
    subcategory = product.subcategory

    # Получите список всех товаров из той же подкатегории, исключая текущий товар
    related_products = Product.objects.filter(subcategory=subcategory).exclude(id=product.id)

    # Выберите четыре случайных товара из списка
    random_related_products = sample(list(related_products), min(4, len(related_products)))

    context = {
        'product': product,
        'category': category,
        'random_related_products': random_related_products,
        # 'cart_product_form': cart_product_form,
    }

    return render(request, 'shop/product/product_details.html', context)
