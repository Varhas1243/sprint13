
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import AuthorForm
from .models import Author


@login_required
def author_list(request):
    if request.user.role != 1:
        raise PermissionDenied

    authors = Author.objects.all().prefetch_related("books")

    return render(request, "author/author_list.html", {
        "authors": authors
    })


@login_required
def author_create(request):
    if request.user.role != 1:
        raise PermissionDenied

    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm()

    return render(request, "author/author_form.html", {
        "form": form,
        "page_title": "Додавання автора",
        "submit_label": "Додати автора",
    })


@login_required
def author_update(request, author_id):
    if request.user.role != 1:
        raise PermissionDenied

    author = get_object_or_404(Author, pk=author_id)

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)

        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm(instance=author)

    return render(request, "author/author_form.html", {
        "form": form,
        "author": author,
        "page_title": "Редагування автора",
        "submit_label": "Зберегти зміни",
    })


@login_required
def author_delete(request, author_id):
    if request.user.role != 1:
        raise PermissionDenied

    if request.method != "POST":
        raise PermissionDenied

    author = get_object_or_404(Author, pk=author_id)

    if author.books.exists():
        authors = Author.objects.all().prefetch_related("books")

        return render(request, "author/author_list.html", {
            "authors": authors,
            "error": "Не можна видалити автора, який має книги",
        })

    author.delete()

    return redirect("author_list")
