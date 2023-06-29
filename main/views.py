from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@csrf_exempt
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def about(request):
    return render(request, 'navigations/about.html')

@csrf_exempt
def privacy(request):
    return render(request, 'navigations/privacy.html')

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            'New message from ' + name,
            message,
            email,
            ['your-email@example.com'],
            fail_silently=False,
        )
        return redirect('home')
    return render(request, 'navigations/contact.html')

from django.core.paginator import Paginator

def scoreboard(request):
    users = User.objects.all().order_by('-userprofile__elo')

    paginator = Paginator(users, 10)  # Chia danh sách users thành các trang, mỗi trang có tối đa 10 người dùng
    page_number = request.GET.get('page')  # Lấy số trang hiện tại từ tham số truy vấn 'page'

    page_obj = paginator.get_page(page_number)  # Lấy đối tượng trang hiện tại

    return render(request, 'navigations/scoreboard.html', {'page_obj': page_obj})
