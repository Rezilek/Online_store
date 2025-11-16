from django.urls import path
from .views import (
    HomeView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, ContactsView  # Убедитесь, что ProductDeleteView импортирован
)
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # ДОБАВЬТЕ ЭТУ СТРОКУ
]
