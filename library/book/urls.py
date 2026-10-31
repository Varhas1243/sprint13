
from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/create/", views.book_create, name="book_create"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/<int:book_id>/edit/", views.book_update, name="book_update"),
    path("users/<int:user_id>/books/", views.user_books, name="user_books"),
]
