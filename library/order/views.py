
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .forms import OrderCreateForm, OrderUpdateForm
from .models import Order


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
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            Order.objects.create(
                user=request.user,
                book=form.cleaned_data["book"],
                plated_end_at=timezone.now() + timedelta(days=14),
            )

            return redirect("my_orders")
    else:
        form = OrderCreateForm(initial={"book": request.GET.get("book")})

    return render(request, "order/create_order.html", {
        "form": form
    })


@login_required
def update_order(request, order_id):
    if request.user.role != 1:
        raise PermissionDenied

    order = get_object_or_404(
        Order.objects.select_related("user", "book"),
        pk=order_id,
    )

    if order.end_at is not None:
        raise PermissionDenied

    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, "order/order_form.html", {
        "form": form,
        "order": order,
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
