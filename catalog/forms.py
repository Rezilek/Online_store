from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import os
from django.utils.translation import gettext_lazy as _


class ProductForm(forms.ModelForm):
    # Константы с запрещенными словами
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
        'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Стилизация всех полей
        for field_name, field in self.fields.items():
            # Базовые классы для всех полей
            field.widget.attrs['class'] = 'form-control'

            # Добавляем placeholder
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'

            # Специальная стилизация для определенных полей
            if field_name == 'description':
                field.widget.attrs['rows'] = 4
                field.widget.attrs['class'] += ' form-control-textarea'
            elif field_name == 'price':
                field.widget.attrs['step'] = '0.01'
                field.widget.attrs['min'] = '0'
                field.widget.attrs['class'] += ' form-control-price'
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control form-control-file'
            elif field_name == 'category':
                field.widget.attrs['class'] += ' form-select'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}". '
                    f'Пожалуйста, используйте другое название.'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get('description', '').lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}". '
                    f'Пожалуйста, измените описание.'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены - не может быть отрицательной"""
        price = self.cleaned_data['price']

        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной. Введите положительное значение.')

        return price

    def clean_image(self):
        """Валидация загружаемого изображения"""
        image = self.cleaned_data.get('image')

        if image:
            # Проверка расширения файла
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in valid_extensions:
                raise ValidationError(
                    'Поддерживаются только следующие форматы изображений: JPG, JPEG, PNG, GIF'
                )

            # Проверка размера файла (5 МБ)
            max_size = 5 * 1024 * 1024  # 5 МБ в байтах
            if image.size > max_size:
                raise ValidationError(
                    f'Размер файла не должен превышать 5 МБ. '
                    f'Текущий размер: {image.size / 1024 / 1024:.1f} МБ'
                )

        return image