from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    # Задание по отправке уведомления по электронной почте при успешном создании заказа.
    order = Order.objects.get(id=order_id)
    subject = f'Замовлення № {order.id}'
    message = (f'Дорогий(га) {order.first_name}, \n\n '
               f'Ви успішно оформили замовлення. '
               f'№ вашего замовлення {order.id}')

    mail_sent = send_mail(subject,
                          message,
                          'sunrisebeautybar.info@gmail.com',
                          [order.email])

    return mail_sent
