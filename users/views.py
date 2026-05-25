from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileEditForm, RegistrationForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile", user_id=request.user.id)

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile", user_id=request.user.id)

    if request.method == "POST":
        form = LoginForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("users:profile", user_id=form.get_user().id)
    else:
        form = LoginForm(request)

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")


def profile_view(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("skills"),
        id=user_id,
    )

    return render(
        request,
        "users/user-details.html",
        {"user": profile_user},
    )


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)
            return redirect("users:profile", user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "users/change_password.html",
        {"form": form},
    )

@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("users:profile", user_id=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(
        request,
        "users/edit_profile.html",
        {
            "form": form,
            "user": request.user,
        },
    )
