from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError

from .models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Имя"}),
    )
    surname = forms.CharField(
        label="Фамилия",
        max_length=150,
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
            first_name=self.cleaned_data["name"],
            last_name=self.cleaned_data["surname"],
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