def user_can_manage_project(user, project):
    return user.is_authenticated and (
        user == project.owner or user.is_staff
    )
