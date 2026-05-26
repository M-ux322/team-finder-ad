from urllib.parse import urlparse

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

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")

        if not github_url:
            return github_url

        host = urlparse(github_url).netloc.lower()

        if host not in {"github.com", "www.github.com"}:
            raise forms.ValidationError(
                "Укажите ссылку на репозиторий GitHub."
            )

        return github_url