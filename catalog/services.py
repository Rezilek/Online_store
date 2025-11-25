# catalog/services.py
from django.core.cache import cache
from .models import Product, Category


def get_products_from_cache():
    """
    Получает список всех опубликованных продуктов из кеша или БД
    """
    if cache.get('published_products'):
        print("DEBUG: Products from cache")
        return cache.get('published_products')
    else:
        print("DEBUG: Products from database")
        products = Product.objects.filter(status='published').select_related('category', 'owner')
        cache.set('published_products', list(products), 60 * 15)  # Кешируем на 15 минут
        return products


def get_products_by_category_from_cache(category_id):
    """
    Получает список продуктов по категории из кеша или БД
    """
    cache_key = f'products_category_{category_id}'

    if cache.get(cache_key):
        print(f"DEBUG: Products for category {category_id} from cache")
        return cache.get(cache_key)
    else:
        print(f"DEBUG: Products for category {category_id} from database")
        products = Product.objects.filter(
            category_id=category_id,
            status='published'
        ).select_related('category', 'owner')
        cache.set(cache_key, list(products), 60 * 15)  # Кешируем на 15 минут
        return products


def clear_products_cache():
    """
    Очищает кеш продуктов (вызывать при изменении продуктов)
    """
    cache.delete('published_products')
    # Очищаем кеш для всех категорий
    categories = Category.objects.all()
    for category in categories:
        cache.delete(f'products_category_{category.id}')