from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True, })
    return render(request, 'cart/shop_cart.html', {'cart': cart})


@require_POST
def cart_update(request):
    cart = Cart(request)
    for product_id in cart.cart.keys():
        form = CartAddProductForm(request.POST, prefix=f'cart_item_{product_id}')
        if form.is_valid():
            cd = form.cleaned_data
            cart.update(int(product_id), cd['quantity'])
    return redirect('cart:cart_detail')

"""



def update_cart(request):
    if request.method == 'POST':

        cart = Cart(request)
        for item in cart:
            #print('ITEM', item)
            product_id = item['product'].id  # Получаем идентификатор товара из элемента корзины
            #print('PRODUCT_ID', product_id)
            quantity = request.POST.get(f'cart_item_{product_id}-quantity')

            # quantity = request.POST.get('quantity')
            # print('Received quantity:', str(quantity))
            form = CartUpdateForm(request.POST, prefix=f'cart_item_{product_id}')
            # print('FORM', form)
            if form.is_valid():
                # quantity = form.cleaned_data['quantity']  # Извлекаем количество из формы
                #print('QUANTITY222', quantity)
                cart.update(int(product_id), int(quantity))  # Обновляем количество товара в корзине
                #print('cart', list(cart))
            else:
                # Обработка ошибок, если форма не прошла валидацию
                pass
    return redirect('cart:cart_detail')


def update_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print('Received quantity:', quantity)
        # Ваша текущая логика обновления корзины
    return redirect('cart:cart_detail')"""