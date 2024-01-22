from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    else:
        cart.add(product=product, quantity=1, update_quantity=False)

    # Сохраните информацию о категории или странице в сессии
    category = request.GET.get('category')

    request.session['last_visited_category'] = category

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # Получите информацию о категории или странице из сессии
    category_name = request.session.get('last_visited_category')

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True, })

    coupon_apply_form = CouponApplyForm()

    # Используйте информацию о категории при формировании URL
    continue_shopping_url = reverse('shop:product_list', args=[category_name])

    context = {
        'cart': cart,
        'category_name': category_name,
        'continue_shopping_url': continue_shopping_url,
        'coupon_apply_form': coupon_apply_form,
    }

    return render(request, 'cart/shop_cart.html', context)


@require_POST
def cart_update(request):
    cart = Cart(request)
    for key, value in request.POST.items():
        if key.startswith('cart_item_'):
            product_id, field_name = key.replace('cart_item_', '').split('-')
            if field_name == 'quantity':
                quantity = int(value)
                product = get_object_or_404(Product, id=int(product_id))  # Получить объект Product по его id
                if quantity == 0:
                    cart.remove(product)
                else:
                    cart.update(int(product_id), quantity)
    return redirect('cart:cart_detail')


