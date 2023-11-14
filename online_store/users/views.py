from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserEditForm
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


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
            # Check if the email error exists in the form errors
            if 'email' in form.errors:
                # Add a custom error message using Django's messages framework
                messages.error(request, 'Ця електронна пошта вже використовується.')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


@login_required
def account(request):
    user_data = request.user
    user_orders = Order.objects.filter(user=request.user, paid=True).order_by('-created')[:6]

    return render(request, 'account/account.html', {'user_data': user_data, 'user_orders': user_orders})


@login_required
def edit(request):

    user_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'birth_date': request.user.birth_date,
        'phone': request.user.phone,
        'email': request.user.email,
        'city': request.user.city,
        'department_np': request.user.department_np,
    }
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')

    else:
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
        'user_data': user_data,
        'user': request.user,
    }

    print('context', context)
    return render(request, 'account/edit.html', context)


"""
@login_required
def edit(request):
    user = request.user

    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date,
        'phone': user.phone,
        'email': user.email,
        'city': user.city,
        'department_np': user.department_np,
    }

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            print('user_form.is_valid', user)
            form.save()
            return redirect('account')
    else:
        form = UserEditForm(instance=user)

    context = {
        'form': form,
        'user_data': user_data,  # Добавление имени пользователя в контекст
        'user': request.user
    }

    print('context', context)
    return render(request, 'account/edit.html', context)




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
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'birth_date': request.user.birth_date,
        'email': request.user.email,
        'phone': request.user.phone,
        'city': request.user.city,
        'department_np': request.user.department_np,
        }
    return render(request, 'account/edit.html', context)



@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        print('forma', form)

        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
        'user_data': request.user,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'birth_date': request.user.birth_date,
        'phone': request.user.phone,
        'email': request.user.email,
        'city': request.user.city,
        'department_np': request.user.department_np,
    }
    return render(request, 'account/edit.html', context)

"""