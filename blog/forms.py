from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from blog.models import Blog


class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-primary btn-dark'))

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('slug', 'views_count')