from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, LoginView
from django.core.mail import EmailMessage
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from mail_service_app.models import Mailing
from users.forms import UserRegisterForm, UserPasswordResetForm, UserProfileForm, UserResetConfirmForm
from users.models import User


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.set_is_active'


@permission_required(perm='users.set_is_active')
def change_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:user_list')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        subject = 'Верификация учетной записи'
        message = f'Здравствуйте {user.first_name}, пожалуйста проверьте свою учетную запись, перейдя по этой ссылке: ' \
                  f'http://localhost:8000{reverse_lazy("users:confirm_registration", kwargs={"token": user.token})}.'
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        return response


class ConfirmRegistrationView(View):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user = User.objects.filter(token=token).first()
        if user:
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            return redirect('mail_service:home')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/email_reset_message.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

