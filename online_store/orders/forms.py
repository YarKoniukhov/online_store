from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    order_notes = forms.CharField(required=False,
                                 widget=forms.Textarea(attrs={'placeholder': 'Примітка про ваше замовлення'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'department_np', 'order_notes']


class EmailPostForm(forms.ModelForm):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)