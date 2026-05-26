from django.urls import path

from . import views


app_name = "projects"


urlpatterns = [
    path("", views.project_list_view, name="project_list"),
    path("list", views.project_list_view, name="project_list_alias"),

    path("create-project", views.create_project_view, name="create"),

    path("<int:project_id>/edit", views.edit_project_view, name="edit"),
    path(
        "<int:project_id>/complete",
        views.complete_project_view,
        name="complete",
    ),
    path(
        "<int:project_id>/participate",
        views.participate_project_view,
        name="participate",
    ),
    path(
        "<int:project_id>/favorite",
        views.toggle_favorite_view,
        name="favorite",
    ),
    path("<int:project_id>", views.project_detail_view, name="detail"),
]