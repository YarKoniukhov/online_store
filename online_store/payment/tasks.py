import os
from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    # Задание по отправке уведомления по электронной почте при успешной оплате заказа.
    order = Order.objects.get(id=order_id)

    transaction_info = {
        'stripe_id': order.stripe_id,
    }

    context = {
        'order': order,
        'transaction_info': transaction_info,
        'updated': order.updated
    }
    # Создать электронный счет
    subject = f'Sunrise Beautybar - рахунок No {order.id}'
    message = 'Рахунок-фактура вашої нещодавньої покупки.'
    email = EmailMessage(subject,
                         message,
                         'sunrisebeautybar.info@gmail.com',
                         [order.email, 'sunrisebeautybar.info@gmail.com'])
    # сгенерировать PDF
    html = render_to_string('orders/pdf.html', context)
    out = BytesIO()
    # stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    stylesheets = [weasyprint.CSS(os.path.join(settings.STATIC_ROOT, 'css', 'pdf.css'))]

    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # прикрепить PDF-файл
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    # отправить электронное письмо
    email.send()
