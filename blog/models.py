from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from mail_service_app.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Url', blank=True)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='images/', **NULLABLE, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        print('Saving post:', self.title)
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья '
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
