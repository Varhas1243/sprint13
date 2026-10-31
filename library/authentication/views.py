
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import RegisterForm, UserUpdateForm
from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return redirect("book_list")
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {
        "form": form
    })


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


@login_required
def user_update(request, user_id):
    if request.user.role != 1:
        raise PermissionDenied

    library_user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=library_user)

        if form.is_valid():
            form.save()
            return redirect("user_detail", user_id=library_user.id)
    else:
        form = UserUpdateForm(instance=library_user)

    return render(request, "user/user_form.html", {
        "form": form,
        "library_user": library_user,
    })
