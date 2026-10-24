
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        patronymic = request.POST.get("patronymic", "").strip()

        if not all([name, surname, patronymic]):
            return render(request, "author/author_create.html", {
                "error": "Заповніть усі поля"
            })

        if any(
            len(value) > 20
            for value in [name, surname, patronymic]
        ):
            return render(request, "author/author_create.html", {
                "error": "Максимальна довжина кожного поля — 20 символів"
            })

        Author.objects.create(
            name=name,
            surname=surname,
            patronymic=patronymic,
        )

        return redirect("author_list")

    return render(request, "author/author_create.html")


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
