# catalog/forms.py
from django import forms
from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                   'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:  # Только при создании
            instance.owner = self.user
            instance.status = 'moderation'  # По умолчанию на модерации
        if commit:
            instance.save()
        return instance

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f'Название содержит запрещенное слово: {word}')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f'Описание содержит запрещенное слово: {word}')
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price