from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('brand/<slug:brand_slug>/', views.product_list_by_brand, name='product_list_by_brand'),


    path('product', views.product_list, name='product_list'),

]


"""
    path('product', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<slug:brand_slug>/', views.product_list, name='product_list_by_brand'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    """