from django import forms
from mailings.models import MailingRecipient

class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ["email", "full_name", "comment", "token"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
