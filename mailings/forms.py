from django import forms
from django.contrib.auth import get_user_model

from users.models import CustomUser

User = get_user_model()


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "comment", "token"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
