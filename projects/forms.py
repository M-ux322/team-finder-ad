from django import forms

from core.validators import validate_github_url

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
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Введите название проекта"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Расскажите о цели проекта и необходимой команде"
                    ),
                    "rows": 7,
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project"
                }
            ),
            "status": forms.Select(),
        }

    def clean_github_url(self):
        return validate_github_url(
            self.cleaned_data.get("github_url"),
            "Укажите ссылку на репозиторий GitHub.",
        )
