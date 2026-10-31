from django import forms

from .models import CustomUser

ROLE_FORM_CHOICES = (
    (0, "Читач"),
    (1, "Бібліотекар"),
)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    role = forms.TypedChoiceField(
        label="Роль",
        choices=ROLE_FORM_CHOICES,
        coerce=int,
        initial=0,
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "middle_name", "email", "password", "role"]
        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "middle_name": "По батькові",
            "email": "Email",
        }
        widgets = {
            "email": forms.EmailInput,
        }
        error_messages = {
            "email": {
                "unique": "Користувач із таким email вже існує",
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    role = forms.TypedChoiceField(
        label="Роль",
        choices=ROLE_FORM_CHOICES,
        coerce=int,
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "middle_name", "email", "role", "is_active"]
        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "middle_name": "По батькові",
            "email": "Email",
            "is_active": "Активний",
        }
        widgets = {
            "email": forms.EmailInput,
        }
        error_messages = {
            "email": {
                "unique": "Користувач із таким email вже існує",
            },
        }
