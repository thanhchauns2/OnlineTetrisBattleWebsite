import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from tournament.models import SelectedUser
from .forms import UserSelectionForm

def elimination(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'yes':
            return redirect('/tournament/elimination_choosing')
        else:
            return redirect('/tournament/elimination_eliminating')
        # return HttpResponse(f'Bạn đã chọn: {choice}')
    return render(request, 'tournament/elimination.html')

def elimination_choosing(request):
    form = UserSelectionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        selected_users = form.cleaned_data['users']
        
        # Xóa tất cả các SelectedUser đã tồn tại
        SelectedUser.objects.all().delete()
        
        # Lưu các người dùng được chọn vào cơ sở dữ liệu
        for user in selected_users:
            SelectedUser.objects.create(user=user)
        
        return redirect('/tournament/elimination_eliminating')

    users = User.objects.all().order_by('username')
    return render(request, 'tournament/elimination_choosing.html', {'form': form})

def draw_group(selected_users):
    random.shuffle(selected_users)
    __elimination = selected_users
    return __elimination

def elimination_eliminating(request):
    selected_users = SelectedUser.objects.all()
    __elimination = draw_group(list(selected_users))
    print(__elimination)
    return render(request, 'tournament/elimination_eliminating.html', {'elimination': __elimination})

