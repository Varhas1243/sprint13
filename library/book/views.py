
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import BookForm
from .models import Book
from authentication.models import CustomUser
from order.models import Order


@login_required
def book_list(request):
    books = Book.objects.all().prefetch_related("authors")

    title = request.GET.get("title", "").strip()
    author = request.GET.get("author", "").strip()

    if title:
        books = books.filter(name__icontains=title)

    if author:
        books = books.filter(
            authors__surname__icontains=author
        ).distinct()

    return render(request, "book/book_list.html", {
        "books": books,
        "title": title,
        "author": author,
    })


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.prefetch_related("authors"),
        pk=book_id,
    )

    return render(request, "book/book_detail.html", {
        "book": book
    })


@login_required
def book_create(request):
    if request.user.role != 1:
        raise PermissionDenied

    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm()

    return render(request, "book/book_form.html", {
        "form": form,
        "page_title": "Додавання книги",
        "submit_label": "Додати книгу",
    })


@login_required
def book_update(request, book_id):
    if request.user.role != 1:
        raise PermissionDenied

    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "book/book_form.html", {
        "form": form,
        "book": book,
        "page_title": "Редагування книги",
        "submit_label": "Зберегти зміни",
    })


@login_required
def user_books(request, user_id):
    if request.user.role != 1:
        raise PermissionDenied

    library_user = get_object_or_404(CustomUser, pk=user_id)

    orders = Order.objects.filter(
        user=library_user,
        end_at__isnull=True,
    ).select_related("book").order_by("-created_at")

    return render(request, "book/user_books.html", {
        "library_user": library_user,
        "orders": orders,
    })
