from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField('Прізвище', max_length=50)
    # phone_num = models.
    email = models.EmailField()
    city = models.CharField('Місто', max_length=100)

    address = models.CharField('Адреса', max_length=250)
