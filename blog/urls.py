from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
]