from abc import ABC
from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy

from blog.models import Blog
from .forms import MailingForm, ClientForm, MessageForm
from .models import Client, Mailing, Message, MailingLog


class HomeView(TemplateView):
    template_name = 'mail_service/home.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['active_mailing_count'] = Mailing.objects.filter(mailing_status=Mailing.STARTED).count()
        context_data['count_clients'] = Client.objects.distinct().count()
        context_data['blog_posts'] = sample(list(Blog.objects.all()), 3)
        return context_data


class ClientListView(LoginRequiredMixin,ListView):
    model = Client
    template_name = 'mail_service/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail_service_app.set_mailing_status'):
            return queryset

        return queryset.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail_service:client_list')
    template_name = 'mail_service/client_create.html'
    extra_context = {'title': 'Создание клиентов', 'submit_label': 'Создать'}

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['full_name', 'email', 'comments']
    template_name_suffix = 'mail_service/client_update.html'
    success_url = reverse_lazy('mail_service_app:client_list')
    extra_context = {'title': 'Изменить данные клиента'}

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return user.is_authenticated and (client.user == user or user.has_perm('mail_service_app.change_client'))


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mail_service:client_list')
    extra_context = {'title': 'Удалить клиента'}

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return self.request.user.is_authenticated and (client.user == user or user.has_perm('mail_service_app'
                                                                                            '.delete_client'))


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    queryset = Mailing.objects.all()
    template_name = 'mail_service/mailing_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing_app.view_mailing'):
            return queryset

        return queryset.filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = 'mail_service/mailing_form.html'
    form_class = MailingForm
    success_url = '/mailing_list/'
    extra_context = {'title': 'Создание сообщения', 'submit_label': 'Создать'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mail_service/mailing_detail.html'
    context_object_name = 'mailing'
    extra_context = {'title': 'Детали рассылки'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm('mail_service_app.view_mailing') or self.request.user == self.object.user:
            return self.object
        raise HttpResponseForbidden


class MailingUpdateView(UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mail_service/mailing_update.html'
    success_url = reverse_lazy('mail_service:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user.is_authenticated and (mailing.user == user or user.has_perm('mail_service_app.change_mailing'))


class MailingDeleteView(UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail_service:mailing_list')
    extra_context = {'title': 'Удалить рассылку'}

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_perm('mail_service_app.delete_mailing')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mail_service/message_detail.html'
    extra_context = {'title': 'Детали сообщения'}


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_service:message_list')
    template_name = 'mail_service/message_create.html'
    extra_context = {'title': 'Сообщение'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mail_service/message_update.html'
    success_url = reverse_lazy('mail_service:message_list')

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('mail_service_app.change_message'))


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mail_service:message_list')
    extra_context = {'title': 'Удалить сообщение'}

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('mail_service_app.delete_message'))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail_service/message_list.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail_service_app.view_message'):
            return queryset

        return queryset.filter(user=self.request.user)


class LogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mail_service/log_list.html'
    context_object_name = 'log_list'
