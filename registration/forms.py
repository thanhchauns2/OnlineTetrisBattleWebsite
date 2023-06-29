from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First name:',
        help_text='. Letters only.'
    )
    last_name = forms.CharField(
        label='Last name:',
        help_text='. Letters only.'
    )
    username = forms.CharField(
        label='Username:',
        help_text='. Letters, digits and @/./+/-/_ only.'
    )
    email = forms.EmailField(
        label='Email:',
        help_text='We will send an email for verification.'
    )
    account_type = forms.CharField(
        label='References:',
        help_text='If you\'re not sure what to fill in this field, enter your username instead'
    )
    password1 = forms.CharField(
        label='Password:',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Your password must contain at least 6 characters.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'account_type', 'first_name', 'last_name', 'password1', 'password2']
