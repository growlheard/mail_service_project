from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import BlogForm
from .models import Blog
from .services import cache_blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    queryset = Blog.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog_list'] = cache_blog()
        return context_data


@permission_required('blog.change_blog')
def change_blog_status(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.is_published = not blog.is_published
    blog.save()
    return redirect('blog:blog_list')


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    queryset = Blog.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.increase_views_count(slug)
        return super().get(request, *args, **kwargs)

    def increase_views_count(self, slug):
        blog = get_object_or_404(Blog, slug=slug)
        blog.views_count += 1
        blog.save()


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    form_class = BlogForm

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:blog_list')
