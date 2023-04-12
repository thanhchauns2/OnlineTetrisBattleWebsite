from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('configurations/', views.configurations, name='configurations'),
]