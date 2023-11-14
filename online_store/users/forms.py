from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    birth_date = forms.DateField(required=False, help_text='Дата народження')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'birth_date', 'phone', 'email', 'city',
                  'department_np', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email вже використовується.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Устанавливаем first_name в качестве username
        user.username = self.cleaned_data['first_name']

        if commit:
            user.save()
        return user


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birth_date', 'phone', 'email', 'city', 'department_np')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].required = False

    def clean_email(self):
        data = self.cleaned_data['email']
        # Проверяем, что пользователь только создается (self.instance.id равен None)
        if self.instance.id is None:
            existing_user = User.objects.filter(email=data).first()
            if existing_user:
                raise forms.ValidationError('Email вже використовується.')
        return data
