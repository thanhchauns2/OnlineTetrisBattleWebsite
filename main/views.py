from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

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