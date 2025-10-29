from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForm
from .models import Product, Contact


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


def product_detail(request, pk):
    """Контроллер для отображения страницы одного товара"""
    # Получаем объект из БД по pk или возвращаем 404
    product = get_object_or_404(Product, pk=pk)

    # Рендерим шаблон с контекстом
    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)


def home(request):
    """Контроллер главной страницы"""
    # ORM-запрос на получение всех продуктов
    products = Product.objects.all()

    # Выводим в консоль для проверки (дополнительное задание из прошлой ДЗ)
    latest_products = products.order_by('-created_at')[:5]
    for product in latest_products:
        print(f"Продукт: {product.name}, Цена: {product.price}")

    context = {
        'products': products  # Передаем все продукты в шаблон
    }
    return render(request, 'catalog/home.html', context)


def add_product(request):
    """Контроллер для добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем на главную после успешного добавления
    else:
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, 'catalog/add_product.html', context)

