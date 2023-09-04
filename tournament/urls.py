from django.urls import path
from . import views

urlpatterns = [
    path('brackets/', views.brackets, name='prepare'),
]