from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import os


def order_create(request):
    cart = Cart(request)
    user_data = None
    order = None  # Инициализация переменной заказа

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user  # Привязываем заказ к текущему пользователю
            else:
                order.user = None  # Если пользователь не авторизован

            # Добавим обработку поля для примечания
            order.order_notes = form.cleaned_data.get('order_notes', '')  # Получаем значение примечания из формы

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистить корзину
            cart.clear()
            # запустить асинхронное задание, отправка уведомления по email о заказе (orders/tasks.py)
            # order_created.delay(order.id)

            # задать заказ в сеансе
            request.session['order_id'] = order.id
            # перенаправить к платежу
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/checkout_done.html', {'order': order})  # создано до подключения платежей

    else:
        if request.user.is_authenticated:
            user_data = {
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'birth_date': request.user.birth_date,
                'phone': request.user.phone,
                'email': request.user.email,
                'city': request.user.city,
                'department_np': request.user.department_np
            }
            form = OrderCreateForm(initial=user_data)
        else:
            form = OrderCreateForm()

    context = {
        'cart': cart,
        'user_data': user_data,
        'form': form,
    }

    return render(request, 'orders/checkout.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Получение информации о транзакции платежа
    transaction_info = None
    if order.stripe_id:
        transaction_info = {
            'stripe_id': order.stripe_id,
            # Другие данные о транзакции, которые вы хотите добавить
        }

    context = {
        'order': order,
        'transaction_info': transaction_info,  # Включаем информацию о транзакции в контекст
        'updated': order.updated
    }

    html = render_to_string('orders/pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(os.path.join(settings.STATIC_ROOT, 'css', 'pdf.css'))])

    return response
