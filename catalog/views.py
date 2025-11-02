from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


# Главная страница - список товаров
class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Вывод в консоль для дополнительного задания
        latest_products = Product.objects.all().order_by('-created_at')[:5]
        for product in latest_products:
            print(f"Продукт: {product.name}, Цена: {product.price}")
        return context


# Страница одного товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# Страница контактов
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        # Обработка формы обратной связи
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Здесь можно добавить логику отправки email или сохранения в базу
        context = {
            'success_message': f'Спасибо, {name}! Ваше сообщение отправлено.'
        }
        return self.render_to_response(context)


# Форма добавления товара (дополнительное задание из прошлой ДЗ)
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')