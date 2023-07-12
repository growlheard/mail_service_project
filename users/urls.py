from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, ProfileView, ConfirmRegistrationView, UserPasswordResetView, \
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomPasswordResetDoneView, UserListView, \
    change_user_status
app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('confirm-registration/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('user_list/', login_required(UserListView.as_view()), name='user_list'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('users/<int:pk>/status/', change_user_status, name='change_user_status'),


    ]

