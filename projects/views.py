from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import ProjectForm
from .models import Project


def user_can_manage_project(user, project):
    return user.is_authenticated and (
        user == project.owner or user.is_staff
    )

def project_list_view(request):

    projects = (
        Project.objects
        .select_related("owner")
        .order_by("-created_at")
    )

    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "projects/project_list.html",
        {
            "page_obj": page_obj,
        },
    )


@login_required
def create_project_view(request):

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

    project = get_object_or_404(Project, id=project_id)

    if not user_can_manage_project(request.user, project):
        raise PermissionDenied

    project.status = Project.Status.CLOSED
    project.save(update_fields=["status", "updated_at"])

    return redirect("projects:detail", project_id=project.id)


@login_required
@require_POST
def participate_project_view(request, project_id):

    project = get_object_or_404(
        Project.objects.select_related("owner"),
        id=project_id,
    )

    if request.user == project.owner:
        return redirect("projects:detail", project_id=project.id)

    is_participant = project.participants.filter(id=request.user.id).exists()

    if is_participant:
        project.participants.remove(request.user)
    elif project.status == Project.Status.OPEN:
        project.participants.add(request.user)

    return redirect("projects:detail", project_id=project.id)