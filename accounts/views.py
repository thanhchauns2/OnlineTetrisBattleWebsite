from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomPasswordChangeForm
from django.conf import settings

@csrf_exempt
def profile(request):
    context = {}
    if settings.UPDATE == True:
        context = {'updating' : 1}
    return render(request, 'accounts/profile.html', context=context)

@csrf_exempt
def configurations(request):
    context = {}
    if settings.UPDATE == True:
        context = {'updating' : 1}
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    context['form'] = form
    return render(request, 'accounts/configurations.html', context=context)