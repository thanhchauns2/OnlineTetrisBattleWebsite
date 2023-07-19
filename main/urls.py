from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('contest_rules/', views.contest_rules, name='contest_rules'),
    path('contact/', views.contact, name='contact'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
]
