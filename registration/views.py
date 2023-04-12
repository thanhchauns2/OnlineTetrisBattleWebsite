from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import random
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.id = random.randint(100000000000000, 999999999999999)
            user.save()
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # Redirect to home page
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def __login(request):
    return LoginView.as_view(template_name='registration/login.html')(request)

def logout_view(request):
    logout(request)
    return redirect('home')