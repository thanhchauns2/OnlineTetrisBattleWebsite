from django.urls import path
from . import views

urlpatterns = [
    path('elimination/', views.elimination, name='elimination'),
    path('elimination_choosing/', views.elimination_choosing, name='elimination_choosing'),
    path('elimination_eliminating/', views.elimination_eliminating, name='elimination_eliminating'),
]