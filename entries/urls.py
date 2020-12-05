from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='blog-home'),
    path('entry/<str:entry_slug>/', detail_view, name='entry-detail'),
    path('create_entry/', add_blog_view, name='create-entry'),
    path('edit_entry/<int:pk>/', edit_blog_view, name='edit-entry'),
    path('delete_entry/<int:pk>/', delete_blog_view, name='delete-entry'),
]
