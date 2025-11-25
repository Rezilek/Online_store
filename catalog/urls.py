# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('contacts/', views.contacts, name='contacts'),
    path('moderation/', views.product_moderation, name='product_moderation'),
    path('product/<int:pk>/status/<str:status>/', views.change_product_status, name='change_product_status'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
]