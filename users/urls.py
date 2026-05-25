from django.urls import path

from . import views


app_name = "users"


urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("edit-profile", views.edit_profile_view, name="edit_profile"),

    path("skills/", views.skill_search_view, name="skill_search"),
    path("<int:user_id>/skills/add/", views.add_skill_view, name="add_skill"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        views.remove_skill_view,
        name="remove_skill",
    ),

    path("<int:user_id>/", views.profile_view, name="profile"),
]