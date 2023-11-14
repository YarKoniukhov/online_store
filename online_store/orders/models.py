from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField("Ім'я", max_length=50, blank=False)
    last_name = models.CharField('Прізвище', max_length=50, blank=False)
    phone = models.CharField('Телефон', max_length=20, blank=False)
    email = models.EmailField('Email', blank=False)
    city = models.CharField('Місто', max_length=100, blank=False)
    department_np = models.CharField('№ нової пошти', max_length=250, blank=False)
    created = models.DateTimeField('Створено', auto_now_add=True)
    updated = models.DateTimeField('Оновлено', auto_now=True)
    paid = models.BooleanField('Оплата', default=False)
    order_notes = models.TextField('Примітка до замовлення', blank=True)

    stripe_id = models.CharField(max_length=250, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', null=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Замовлення {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            # никаких ассоциированных платежей
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # путь Stripe для тестовых платежей
            path = '/test/'
        else:
            # путь Stripe для настоящих платежей
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
