from django.contrib import admin
from .models import Client, Mailing, Message, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email','comments',)
    list_filter = ('full_name',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'mailing_status', 'frequency')
    list_filter = ('title', 'mailing_status', 'frequency')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    list_filter = ('title', 'content')


@admin.register(MailingLog)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'sent_at', 'status', 'error_message',)
    list_filter = ('mailing', 'sent_at', 'status', 'error_message',)
