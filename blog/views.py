from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail  # ДОБАВЛЯЕМ ИМПОРТ
from django.conf import settings  # ДОБАВЛЯЕМ ИМПОРТ
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Фильтруем только опубликованные записи
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Получаем объект и увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        old_views = obj.views_count
        obj.views_count += 1
        obj.save()

        # Проверяем достижение 100 просмотров
        if old_views == 99:  # Было 99, стало 100
            self.send_congratulation_email(obj)

        return obj

    def send_congratulation_email(self, post):
        """Отправка email при достижении 100 просмотров"""
        subject = f'Поздравляем! Статья "{post.title}" достигла 100 просмотров!'
        message = f'''
        Поздравляем!

        Ваша статья "{post.title}" достигла 100 просмотров!

        Статистика:
        - Заголовок: {post.title}
        - Дата создания: {post.created_at}
        - Текущие просмотры: {post.views_count}

        Продолжайте в том же духе!
        '''

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@example.com'],  # Замените на ваш email
                fail_silently=False,
            )
            print(f"Email отправлен для статьи: {post.title}")
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        # Перенаправляем на страницу отредактированной статьи
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')