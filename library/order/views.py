
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import Order
from book.models import Book


@login_required
def order_list(request):
    if request.user.role != 1:
        raise PermissionDenied

    orders = Order.objects.select_related(
        "user", "book"
    ).order_by("-created_at")

    return render(request, "order/order_list.html", {
        "orders": orders
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).select_related("book").order_by("-created_at")

    return render(request, "order/my_orders.html", {
        "orders": orders
    })


@login_required
def create_order(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")

        try:
            book = Book.objects.get(pk=book_id)
        except (Book.DoesNotExist, ValueError, TypeError):
            return render(request, "order/create_order.html", {
                "books": Book.objects.all(),
                "error": "Книгу не знайдено",
            })

        active_orders = Order.objects.filter(
            book=book,
            end_at__isnull=True,
        ).count()

        if active_orders >= book.count:
            return render(request, "order/create_order.html", {
                "books": Book.objects.all(),
                "error": "Немає доступних примірників цієї книги",
            })

        Order.objects.create(
            user=request.user,
            book=book,
            plated_end_at=timezone.now() + timedelta(days=14),
        )

        return redirect("my_orders")

    return render(request, "order/create_order.html", {
        "books": Book.objects.all()
    })


@login_required
def close_order(request, order_id):
    if request.user.role != 1:
        raise PermissionDenied

    if request.method != "POST":
        raise PermissionDenied

    order = get_object_or_404(Order, pk=order_id)

    if order.end_at is None:
        order.end_at = timezone.now()
        order.save(update_fields=["end_at"])

    return redirect("order_list")
