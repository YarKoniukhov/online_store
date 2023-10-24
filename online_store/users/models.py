from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), unique=True)

    birth_date = models.DateField(null=True, blank=False, verbose_name='Дата народження')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')

    def __str__(self):
        return self.username
