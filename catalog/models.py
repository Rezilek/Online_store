# catalog/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    PUBLISH_STATUS_CHOICES = [
        ('published', 'Опубликован'),
        ('moderation', 'На модерации'),
        ('rejected', 'Отклонен'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS_CHOICES,
        default='moderation',
        verbose_name='Статус публикации'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_product_status", "Может менять статус продукта"),
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"