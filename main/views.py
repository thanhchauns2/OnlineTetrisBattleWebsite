from django.shortcuts import render, redirect
from django.core.mail import send_mail

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'navigations/about.html')

def privacy(request):
    return render(request, 'navigations/privacy.html')

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