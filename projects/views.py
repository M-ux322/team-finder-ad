from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


def user_can_manage_project(user, project):
    """Проверяет, может ли пользователь управлять проектом."""
    return user.is_authenticated and (
        user == project.owner or user.is_staff
    )


@login_required
def create_project_view(request):
    """Создание нового проекта авторизованным пользователем."""

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            # Автор сразу считается участником собственного проекта.
            project.participants.add(request.user)

            return redirect("projects:detail", project_id=project.id)
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


def project_detail_view(request, project_id):
    """Публичная страница отдельного проекта."""

    project = get_object_or_404(
        Project.objects
        .select_related("owner")
        .prefetch_related("participants"),
        id=project_id,
    )

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
        },
    )


@login_required
def edit_project_view(request, project_id):
    """Редактирование проекта его автором или администратором."""

    project = get_object_or_404(Project, id=project_id)

    if not user_can_manage_project(request.user, project):
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("projects:detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": True,
            "project": project,
        },
    )


@login_required
@require_POST
def complete_project_view(request, project_id):
    """Закрывает проект. Доступно автору или администратору."""

    project = get_object_or_404(Project, id=project_id)

    if not user_can_manage_project(request.user, project):
        raise PermissionDenied

    project.status = Project.Status.CLOSED
    project.save(update_fields=["status", "updated_at"])

    return redirect("projects:detail", project_id=project.id)


@login_required
@require_POST
def participate_project_view(request, project_id):
    """Добавляет пользователя в участники проекта или убирает его."""

    project = get_object_or_404(
        Project.objects.select_related("owner"),
        id=project_id,
    )

    # Автор всегда остаётся участником своего проекта.
    if request.user == project.owner:
        return redirect("projects:detail", project_id=project.id)

    # В закрытый проект нельзя вступить, но уже вступивший может выйти.
    is_participant = project.participants.filter(id=request.user.id).exists()

    if is_participant:
        project.participants.remove(request.user)
    elif project.status == Project.Status.OPEN:
        project.participants.add(request.user)

    return redirect("projects:detail", project_id=project.id)