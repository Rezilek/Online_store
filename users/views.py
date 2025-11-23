from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserProfileForm
from .models import User
from django.contrib.auth.views import LoginView


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # отправка приветственного письма
        user_email = form.cleaned_data.get('email')
        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message='Благодарим за регистрацию в нашем магазине. Теперь вы можете добавлять и редактировать товары.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True