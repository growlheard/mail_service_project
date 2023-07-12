from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from mail_service_app.models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-primary btn-dark'))

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user',)


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить ', css_class='btn btn-primary btn-dark form-control'))

    class Meta:
        model = Mailing
        fields = ['title', 'clients', 'mailing_status', 'frequency']


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-primary btn-dark'))

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('user', 'default_manager')
