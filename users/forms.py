import re
from urllib.parse import urlparse

from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError

from .models import User


def validate_github_url(value):

    if not value:
        return value

    host = urlparse(value).netloc.lower()

    if host not in {"github.com", "www.github.com"}:
        raise forms.ValidationError(
            "Укажите ссылку на профиль GitHub."
        )

    return value


def normalize_phone(value):

    if not value:
        return None

    phone = value.strip().replace(" ", "").replace("-", "")

    if re.fullmatch(r"8\d{10}", phone):
        return "+7" + phone[1:]

    if re.fullmatch(r"\+7\d{10}", phone):
        return phone

    raise forms.ValidationError(
        "Введите номер в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
    )


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=124,
        widget=forms.TextInput(attrs={"placeholder": "Имя"}),
    )
    surname = forms.CharField(
        label="Фамилия",
        max_length=124,
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"}),
    )
    email = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким адресом электронной почты уже существует."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        try:
            password_validation.validate_password(password)
        except ValidationError as error:
            raise forms.ValidationError(error.messages)

        return password

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
        )


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(
                self.request,
                username=email,
                password=password,
            )

            if self.user is None:
                raise forms.ValidationError(
                    "Неверный адрес электронной почты или пароль."
                )

            if not self.user.is_active:
                raise forms.ValidationError(
                    "Этот аккаунт заблокирован."
                )

        return cleaned_data

    def get_user(self):
        return self.user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "name",
            "surname",
            "avatar",
            "about",
            "email",
            "phone",
            "github_url",
        )
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "email": "Адрес электронной почты",
            "phone": "Телефон",
            "github_url": "GitHub",
        }
        widgets = {
            "name": forms.TextInput(),
            "surname": forms.TextInput(),
            "avatar": forms.FileInput(),
            "about": forms.Textarea(attrs={"rows": 5}),
            "email": forms.EmailInput(),
            "phone": forms.TextInput(
                attrs={"placeholder": "+79991234567"}
            ),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/username"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        duplicate_email = User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk)

        if duplicate_email.exists():
            raise forms.ValidationError(
                "Пользователь с таким адресом электронной почты уже существует."
            )

        return email

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data.get("phone"))

        if not phone:
            return None

        duplicate_phone = User.objects.filter(
            phone=phone
        ).exclude(pk=self.instance.pk)

        if duplicate_phone.exists():
            raise forms.ValidationError(
                "Пользователь с таким номером телефона уже существует."
            )

        return phone

    def clean_github_url(self):
        return validate_github_url(
            self.cleaned_data.get("github_url")
        )