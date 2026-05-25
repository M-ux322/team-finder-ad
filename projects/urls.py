from django.urls import path

from . import views


app_name = "projects"


urlpatterns = [
    path("create-project", views.create_project_view, name="create"),
    path("<int:project_id>", views.project_detail_view, name="detail"),
]
