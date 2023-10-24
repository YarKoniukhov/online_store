from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreationForm


# Create your views here.
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                # Создаем нового пользователя и сохраняем его
                form.save()
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=password)
                login(request, user)
                return redirect('shop:index')
        else:
            form = UserCreationForm()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)
