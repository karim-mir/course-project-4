from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import CustomUser


# Форма для создания пользователя в админке
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "role")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Форма для изменения пользователя в админке
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Пароль")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "full_name",
            "role",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def clean_password(self):
        return self.initial["password"]


# Кастомный класс админки
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "full_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("full_name", "role", "token", "comment")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email", "full_name")


# Регистрируем кастомного пользователя с кастомным админом
admin.site.register(CustomUser, CustomUserAdmin)
