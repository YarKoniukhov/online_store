import math
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from orders.models import OrderItem
from .models import Category, Brand, Product, Reviews
from django.db.models import Q, Min, Max
from random import sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .recommender import Recommender
from django.db.models import Count
from .forms import ReviewForm


def index(request):
    latest_products = Product.objects.order_by('-created')[:8]

    popular_products = OrderItem.objects.values('product').annotate(
        total_purchases=Count('product')).order_by('-total_purchases')[:9]

    # Разбиваем товары на группы по три
    group_size = 3
    grouped_products = [popular_products[i:i + group_size] for i in range(0, len(popular_products), group_size)]

    # Получаем три группы товаров
    # топ-товаров, которые были наиболее часто куплены в заказах.
    top_products = Product.objects.filter(id__in=[item['product'] for item in grouped_products[0]])
    best_seller = Product.objects.filter(id__in=[item['product'] for item in grouped_products[1]])
    feature = Product.objects.filter(id__in=[item['product'] for item in grouped_products[2]])

    context = {
        'latest_products': latest_products,
        'top_products': top_products,
        'best_seller': best_seller,
        'feature': feature,
    }
    return render(request, 'shop/index.html', context)


def product_list(request, category_name, brand_id=None):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category).order_by('-created')
    subcategories = category.subcategories.all()
    brands = Brand.objects.filter(product__category=category).distinct()

    selected_subcategories = request.GET.getlist('subcategory')
    all_subcategories_selected = 'all' in request.GET

    selected_brands = request.GET.getlist('brand')
    all_brands_selected = 'all_brands' in request.GET

    if all_subcategories_selected:
        selected_subcategories = [str(subcategory.id) for subcategory in subcategories]

    if all_brands_selected:
        selected_brands = [str(brand.id) for brand in brands]

    query = Q()

    if selected_subcategories:
        query &= Q(subcategory__id__in=selected_subcategories)

    if selected_brands:
        query &= Q(brand__id__in=selected_brands)

    # Добавляем обработку brand_id, если он предоставлен
    if brand_id:
        brand = get_object_or_404(Brand, name=brand_id)
        products = products.filter(brand=brand)

    min_price = int(products.aggregate(Min('price'))['price__min'])
    max_price = int(products.aggregate(Max('price'))['price__max'])

    base_price = min_price - (min_price % 100)
    ceiled_max_price = math.ceil(max_price / 100) * 100

    price_intervals = []
    while base_price <= ceiled_max_price:
        price_label = f"{base_price}-{min(base_price + 100, ceiled_max_price)}"
        price_intervals.append({'min': base_price, 'max': min(base_price + 100, ceiled_max_price), 'label': price_label})
        base_price += 100

    # Если верхняя граница последнего интервала равна или превышает максимальную цену, удаляем последний интервал
    if price_intervals and price_intervals[-1]['max'] >= max_price:
        price_intervals.pop()

    if query:
        products = products.filter(query)

    selected_price_ranges = request.GET.getlist('price_range')
    if selected_price_ranges:
        price_query = Q()
        for price_range in selected_price_ranges:
            min_price, max_price = map(int, price_range.split('-'))
            price_query |= Q(price__gte=min_price, price__lte=max_price)

            for interval in price_intervals:
                if f"{min_price}-{max_price}" == interval['label']:
                    interval['range_selected'] = True

        products = products.filter(price_query)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    current_page = page_obj.number
    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, paginator.num_pages)
    page_range = range(start_page, end_page + 1)

    context = {
        'products': page_obj,
        'page_range': page_range,
        'category': category,
        'subcategories': subcategories,
        'selected_subcategories': selected_subcategories,
        'all_subcategories_selected': all_subcategories_selected,
        'brands': brands,
        'selected_brands': selected_brands,
        'all_brands_selected': all_brands_selected,
        'min_price': min_price,
        'max_price': max_price,
        'category_name': category_name,
        'price_intervals': price_intervals,
    }

    return render(request, 'shop/product/product_list.html', context)


def product_detail(request, id, url):
    product = get_object_or_404(Product, id=id, url=url, available=True)
    category = product.category  # Получаем категорию продукта
    user_data = request.user

    # Получение количества отзывов для конкретного продукта
    review_count = Reviews.objects.filter(product=product).count()

    # Получите подкатегорию текущего товара
    subcategory = product.subcategory

    # Получите список всех товаров из той же подкатегории, исключая текущий товар
    related_products = Product.objects.filter(subcategory=subcategory).exclude(id=product.id)

    # Выберите четыре случайных товара из списка
    random_related_products = sample(list(related_products), min(4, len(related_products)))

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    context = {
        'product': product,
        'category': category,
        'random_related_products': random_related_products,
        'recommended_products': recommended_products,
        'user_data': user_data,
        'review_count': review_count,
    }

    return render(request, 'shop/product/product_details.html', context)


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())

