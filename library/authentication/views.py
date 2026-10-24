
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        middle_name = request.POST.get("middle_name", "").strip()
        role = request.POST.get("role", "0")

        if not all([email, password, first_name, last_name, middle_name]):
            return render(request, "authentication/register.html", {
                "error": "Заповніть усі поля"
            })

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "authentication/register.html", {
                "error": "Користувач із таким email вже існує"
            })

        if role not in ("0", "1"):
            role = "0"

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=int(role),
            is_active=True,
        )

        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return redirect("book_list")

    return render(request, "authentication/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("book_list")

        return render(request, "authentication/login.html", {
            "error": "Неправильний email або пароль"
        })

    return render(request, "authentication/login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("book_list")


@login_required
def user_list(request):
    if request.user.role != 1:
        raise PermissionDenied

    users = CustomUser.objects.all().order_by("id")

    return render(request, "user/user_list.html", {
        "users": users
    })


@login_required
def user_detail(request, user_id):
    if request.user.role != 1:
        raise PermissionDenied

    library_user = get_object_or_404(CustomUser, pk=user_id)

    return render(request, "user/user_detail.html", {
        "library_user": library_user
    })
