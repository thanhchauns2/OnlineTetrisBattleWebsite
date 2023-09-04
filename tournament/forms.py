from django import forms
from django.contrib.auth.models import User

class UserSelectionForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('username'),
        widget=forms.CheckboxSelectMultiple,
        label="Danh sách thí sinh",
    )