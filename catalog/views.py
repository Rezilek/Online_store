from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Контроллер главной страницы"""
    return render(request, 'catalog/home.html')


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

