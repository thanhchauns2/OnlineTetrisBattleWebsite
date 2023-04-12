from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label=("New password"),
        strip=False,
        help_text="",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        fields = ["old_password", "new_password1", "new_password2"]