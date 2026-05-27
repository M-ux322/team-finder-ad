from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.services import paginate_queryset

from .forms import ProjectForm
from .models import Project
from .services import user_can_manage_project


def project_list_view(request):
    projects = (
        Project.objects
        .filter(status=Project.Status.OPEN)
        .select_related("owner")
        .prefetch_related("participants", "favorites")
        .order_by("-created_at")
    )

    return render(
        request,
        "projects/project_list.html",
        {
            "page_obj": paginate_queryset(request, projects),        },
    )


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)

        return redirect("projects:detail", project_id=project.id)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects
        .select_related("owner")
        .prefetch_related("participants", "favorites"),
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
    project = get_object_or_404(Project, id=project_id)

    if not user_can_manage_project(request.user, project):
        raise PermissionDenied

    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect("projects:detail", project_id=project.id)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "project": project,
            "is_edit": True,
        },
    )


@login_required
@require_POST
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not user_can_manage_project(request.user, project):
        raise PermissionDenied

    project.status = Project.Status.CLOSED
    project.save(update_fields=("status",))

    return redirect("projects:detail", project_id=project.id)


@login_required
@require_POST
def participate_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner == request.user:
        return redirect("projects:detail", project_id=project.id)

    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
    elif project.status == Project.Status.OPEN:
        project.participants.add(request.user)

    return redirect("projects:detail", project_id=project.id)


@login_required
@require_POST
def toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.favorites.filter(id=request.user.id).exists():
        project.favorites.remove(request.user)
    else:
        project.favorites.add(request.user)

    next_url = request.POST.get("next")

    if next_url:
        return redirect(next_url)

    return redirect("projects:detail", project_id=project.id)
