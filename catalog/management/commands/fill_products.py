from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми продуктами и категориями'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('База данных очищена')

        # Создаем категории
        categories_data = [
            {
                'name': 'Электроника',
                'description': 'Современная электроника и гаджеты'
            },
            {
                'name': 'Одежда',
                'description': 'Модная одежда и аксессуары'
            },
            {
                'name': 'Книги',
                'description': 'Художественная и учебная литература'
            },
            {
                'name': 'Спорт',
                'description': 'Спортивные товары и инвентарь'
            },
            {
                'name': 'Дом и сад',
                'description': 'Товары для дома и сада'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'Создана категория: {category.name}')

        # Создаем продукты
        products_data = [
            {
                'name': 'Смартфон iPhone 15',
                'description': 'Новый iPhone с улучшенной камерой',
                'category': categories['Электроника'],
                'price': 89999.99
            },
            {
                'name': 'Ноутбук Dell XPS',
                'description': 'Мощный ноутбук для работы и игр',
                'category': categories['Электроника'],
                'price': 129999.99
            },
            {
                'name': 'Футболка хлопковая',
                'description': 'Комфортная футболка из 100% хлопка',
                'category': categories['Одежда'],
                'price': 1499.99
            },
            {
                'name': 'Джинсы классические',
                'description': 'Стильные джинсы прямого кроя',
                'category': categories['Одежда'],
                'price': 3999.99
            },
            {
                'name': 'Python для начинающих',
                'description': 'Лучший учебник по Python',
                'category': categories['Книги'],
                'price': 2499.99
            },
            {
                'name': 'Футбольный мяч',
                'description': 'Профессиональный футбольный мяч',
                'category': categories['Спорт'],
                'price': 2999.99
            },
            {
                'name': 'Горшок для цветов',
                'description': 'Керамический горшок для растений',
                'category': categories['Дом и сад'],
                'price': 899.99
            }
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Создан продукт: {product.name} - {product.price} руб.'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {Category.objects.count()} категорий и {Product.objects.count()} продуктов'
            )
        )
