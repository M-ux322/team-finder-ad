from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "github_url",
            "status",
        )
        labels = {
            "name": "Название проекта",
            "description": "Описание проекта",
            "github_url": "Ссылка на GitHub",
            "status": "Статус проекта",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Введите название проекта"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Расскажите о цели проекта и необходимой команде",
                    "rows": 7,
                }
            ),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/username/project"}
            ),
            "status": forms.Select(),
        }