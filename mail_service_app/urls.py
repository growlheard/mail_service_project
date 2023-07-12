from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import MailServiceAppConfig
from .views import (
    ClientCreateView,
    MailingCreateView,
    MailingDetailView,
    MailingListView,
    HomeView, ClientUpdateView, ClientDeleteView, MailingUpdateView, MailingDeleteView,
    MessageDetailView, ClientListView, MessageCreateView, MessageListView, MessageDeleteView,
    MessageUpdateView, LogListView,
)
# URLs
app_name = MailServiceAppConfig.name

urlpatterns = [
    path('', cache_page(60)(HomeView.as_view()), name='home'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('log/list/', LogListView.as_view(), name='log_list'),
]