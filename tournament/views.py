from django.shortcuts import render
from django.http import HttpResponse

def brackets(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'yes':
            return render(request, 'tournament/brackets_choosing.html')
        else:
            return render(request, 'tournament/brackets_eliminating.html')
        # return HttpResponse(f'Bạn đã chọn: {choice}')
    return render(request, 'tournament/brackets.html')

def brackets_participants(request):
    return render(request, 'tournament/brackets_choosing.html')

def brackets_eliminating(request):
    return render(request, 'tournament/brackets_eliminating.html')
