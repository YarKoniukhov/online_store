from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserEditForm
from .models import User


class Register(View):
    template_name = 'account/register.html'

    def get(self, request):
        context = {
            'form': UserRegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('shop:index')
        else:
            form = UserRegistrationForm()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


@login_required
def account(request):
    # Передаем данные пользователя в контекст
    user_data = {
        'username': request.user.username,
        'last_name': request.user.last_name,
        'birth_date': request.user.birth_date,
        'phone': request.user.phone,
        'email': request.user.email,
        'city': request.user.city,
        'department_np': request.user.department_np
    }

    context = {
        'user_data': user_data
    }

    return render(request, 'account/account.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
        'user_data': request.user
    }

    return render(request, 'account/edit.html', context)

