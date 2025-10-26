from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def contacts(request):
    """Контроллер страницы контактов"""
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Здесь можно добавить логику сохранения в базу данных
        # или отправки email

        # Выводим сообщение об успешной отправке
        context = {
            'success_message': f'Спасибо, {name}! Ваше сообщение отправлено.'
        }
        return render(request, 'catalog/contacts.html', context)

    return render(request, 'catalog/contacts.html')


def home(request):
    """Контроллер главной страницы"""
    # Получаем последние 5 продуктов
    latest_products = Product.objects.all().order_by('-created_at')[:5]

    # Выводим в консоль (для проверки)
    for product in latest_products:
        print(f"Продукт: {product.name}, Цена: {product.price}")

    context = {
        'latest_products': latest_products
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер страницы контактов"""
    # Получаем контактные данные из базы
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Сохраняем в базу данных
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        context = {
            'success_message': f'Спасибо, {name}! Ваше сообщение отправлено.',
            'contact_info': contact_info
        }
        return render(request, 'catalog/contacts.html', context)

    context = {
        'contact_info': contact_info
    }
    return render(request, 'catalog/contacts.html', context)
