# catalog/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create moderator groups with permissions'

    def handle(self, *args, **options):
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем разрешения для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Добавляем разрешения
        permissions = [
            'can_unpublish_product',
            'can_change_product_status',
            'delete_product',  # Удаление любого продукта
            'view_product',  # Просмотр продуктов
            'change_product',  # Изменение продуктов
        ]

        for perm_codename in permissions:
            try:
                perm = Permission.objects.get(content_type=content_type, codename=perm_codename)
                moderator_group.permissions.add(perm)
                self.stdout.write(f'Added permission: {perm_codename}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found'))

        self.stdout.write(
            self.style.SUCCESS('Successfully created "Модератор продуктов" group with permissions')
        )

        # Создаем группу "Контент-менеджер" (дополнительное задание)
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')

        # Получаем разрешения для блога (если есть модель BlogPost)
        try:
            blog_content_type = ContentType.objects.get(app_label='blog', model='blogpost')
            blog_permissions = Permission.objects.filter(content_type=blog_content_type)
            content_manager_group.permissions.add(*blog_permissions)
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Контент-менеджер" group with blog permissions')
            )
        except ContentType.DoesNotExist:
            self.stdout.write(self.style.WARNING('Blog model not found, skipping content manager permissions'))