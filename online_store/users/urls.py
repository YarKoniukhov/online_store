from django.urls import path, include
from .views import Register, account, edit


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),

    path('account/', account, name='account'),
    path('edit/', edit, name='edit'),
]
