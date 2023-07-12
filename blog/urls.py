from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, change_blog_status

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('<slug:slug>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('<int:pk>/change_status/', change_blog_status, name='blog_change_status'),
]