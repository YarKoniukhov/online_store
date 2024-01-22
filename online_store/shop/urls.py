from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('<int:id>/<slug:url>/', views.product_detail, name='product_detail'),
    path('<str:category_name>/', views.product_list, name='product_list'),
    path('<str:category_name>/<str:brand_id>/', views.product_list, name='product_list_brand'),
    path('', views.index, name='index'),
]
