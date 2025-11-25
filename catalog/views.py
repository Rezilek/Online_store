# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm


def home(request):
    # Показываем только опубликованные товары на главной
    featured_products = Product.objects.filter(status='published')[:3]
    return render(request, 'catalog/home.html', {
        'featured_products': featured_products
    })


def product_list(request):
    # Показываем только опубликованные товары
    products = Product.objects.filter(status='published')
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(user=request.user)
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверяем права: только владелец может редактировать
    if product.owner != request.user:
        return HttpResponseForbidden("У вас нет прав для редактирования этого продукта")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product, user=request.user)
    return render(request, 'catalog/product_form.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверяем права: владелец ИЛИ модератор
    is_owner = product.owner == request.user
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

    if not (is_owner or is_moderator):
        return HttpResponseForbidden("У вас нет прав для удаления этого продукта")

    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'object': product})


def contacts(request):
    if request.method == 'POST':
        return render(request, 'catalog/contacts.html', {'success': True})
    return render(request, 'catalog/contacts.html')


# Дополнительные представления для модерации
@login_required
def product_moderation(request):
    # Только для модераторов
    if not request.user.groups.filter(name='Модератор продуктов').exists():
        return HttpResponseForbidden("У вас нет прав для модерации продуктов")

    products = Product.objects.filter(status='moderation')
    return render(request, 'catalog/product_moderation.html', {'products': products})


@login_required
def change_product_status(request, pk, status):
    # Только для модераторов
    if not request.user.groups.filter(name='Модератор продуктов').exists():
        return HttpResponseForbidden("У вас нет прав для изменения статуса продукта")

    product = get_object_or_404(Product, pk=pk)
    if status in ['published', 'rejected']:
        product.status = status
        product.save()

    return redirect('catalog:product_moderation')