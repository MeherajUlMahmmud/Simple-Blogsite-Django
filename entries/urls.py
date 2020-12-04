from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='blog-home'),
    path('entry/<int:pk>/', detail_view, name='entry-detail'),
    path('create_entry/', add_blog_view, name='create-entry'),
    path('edit_entry/<int:pk>/', edit_blog_view, name='edit-entry'),
    path('delete_entry/<int:pk>/', DeleteEntryView.as_view(success_url="/"), name='delete-entry'),
]
