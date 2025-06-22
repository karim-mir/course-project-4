from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser

User = get_user_model()


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "comment", "token"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }


class CustomUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email",)

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
