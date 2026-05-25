from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .forms import LoginForm, ProfileEditForm, RegistrationForm
from .models import User, Skill
import json


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

    is_owner = (
        request.user.is_authenticated
        and request.user.id == profile_user.id
    )

    return render(
        request,
        "users/user-details.html",
        {
            "profile_user": profile_user,
            "is_owner": is_owner,
        },
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


@require_GET
def skill_search_view(request):

    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    skills = (
        Skill.objects
        .filter(name__icontains=query)
        .order_by("name")
        .values("id", "name")[:10]
    )

    return JsonResponse(list(skills), safe=False)


@login_required
@require_POST
def add_skill_view(request, user_id):

    if request.user.id != user_id:
        return JsonResponse(
            {"error": "Нельзя изменять навыки другого пользователя."},
            status=403,
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Некорректные данные запроса."},
            status=400,
        )

    skill_id = data.get("skill_id")
    name = str(data.get("name", "")).strip()

    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    elif name:
        if len(name) > 100:
            return JsonResponse(
                {"error": "Название навыка слишком длинное."},
                status=400,
            )

        skill = Skill.objects.filter(name__iexact=name).first()

        if skill is None:
            skill = Skill.objects.create(name=name)
    else:
        return JsonResponse(
            {"error": "Не указан навык."},
            status=400,
        )

    request.user.skills.add(skill)

    return JsonResponse(
        {
            "id": skill.id,
            "name": skill.name,
        }
    )


@login_required
@require_POST
def remove_skill_view(request, user_id, skill_id):

    if request.user.id != user_id:
        return JsonResponse(
            {"error": "Нельзя изменять навыки другого пользователя."},
            status=403,
        )

    skill = get_object_or_404(Skill, id=skill_id)
    request.user.skills.remove(skill)

    return JsonResponse({"success": True})
