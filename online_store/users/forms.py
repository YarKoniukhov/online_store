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
        fields = ('username', 'last_name', 'birth_date', 'phone', 'email', 'city',
                  'department_np', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'last_name', 'birth_date', 'phone', 'email', 'city', 'department_np']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

        def clean_email(self):
            data = self.cleaned_data['email']
            qs = User.objects.exclude(id=self.instance.id).filter(email=data)
            if qs.exists():
                raise forms.ValidationError('Email вже використовується.')
            return data
