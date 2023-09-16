from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [

    path('', views.index, name='index'),
    path('<str:category_name>/', views.product_list, name='face_list'),

    path('<int:id>/<slug:url>/', views.product_detail, name='product_detail'),
]
