from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from .models import User

class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались! Проверьте вашу почту для подтверждения.'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message='Спасибо за регистрацию в нашем магазине. Мы рады приветствовать вас!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )
        return response

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = '/'