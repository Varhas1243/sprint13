
from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.author_list, name="author_list"),
    path("authors/create/", views.author_create, name="author_create"),
    path(
        "authors/<int:author_id>/delete/",
        views.author_delete,
        name="author_delete",
    ),
]
