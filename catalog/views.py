# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm

def home(request):
    """Главная страница с приветствием и основной информацией"""
    featured_products = Product.objects.all()[:3]  # Показываем первые 3 товара
    return render(request, 'catalog/home.html', {
        'featured_products': featured_products
    })

def product_list(request):
    """Список всех товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def product_detail(request, pk):
    """Детальная информация о товаре"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required
def product_create(request):
    """Создание нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    """Редактирование товара"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    """Удаление товара"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'object': product})

def contacts(request):
    """Страница контактов"""
    if request.method == 'POST':
        # Обработка формы контактов
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Здесь можно добавить логику отправки email или сохранения в БД
        return render(request, 'catalog/contacts.html', {'success': True})
    return render(request, 'catalog/contacts.html')