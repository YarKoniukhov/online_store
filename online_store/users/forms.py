from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'last_name', 'birth_date', 'phone', 'email', 'password1', 'password2')

    birth_date = forms.DateField(required=False, help_text='Дата народження')



"""
 first_name = forms.CharField(max_length=30, required=True, help_text="Ваше ім'я*", label="Username")
    last_name = forms.CharField(max_length=30, required=True, help_text='Ваше прізвище*')
    birth_date = forms.DateField(required=False, help_text='Дата народження')
    phone = forms.CharField(max_length=19, required=True, help_text='Телефон*')
    email = forms.EmailField(max_length=254, required=True, help_text='E-mail*')
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Пароль*')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Повтор пароля*')
"""