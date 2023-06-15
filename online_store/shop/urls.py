from django.urls import path
from . import views


app_name = 'shop'


urlpatterns = [
    path('', views.index, name='index'),
    # path('oblichcha/', views.product_list, name='face_list'),
    path('<str:category_name>/', views.product_list, name='face_list'),

    path('<int:id>/<slug:url>/', views.product_detail, name='product_detail'),
]



"""

    path('product/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('brand/<slug:brand_slug>/', views.product_list, name='product_list_by_brand'),
    # path('product/size/<slug:size_slug>/', views.product_list, name='product_list_by_size'),

    path('product/size/<slug:size_slug>/', views.product_list, name='product_list_by_size'),

    path('product/filter/', views.product_list, name='product_list_by_price'),

    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
"""