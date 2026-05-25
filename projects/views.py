from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


@login_required
def create_project_view(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

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