from django.urls import path, include
from .views import Register, account, edit, order_detail


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('account/', account, name='account'),
    path('edit/', edit, name='edit'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
