from django.urls import path
from . import views

urlpatterns = [
    path('', views.prepare, name='prepare'),
    path('training/', views.training, name='training'),
    path('competition/', views.competition, name='competition'),
    path('tournament/', views.tournament, name='tournament'),
    path('training/single/', views.single, name='single'),
    path('training/duel/', views.duel, name='duel'),
    path('watch/', views.watch, name='watch'),
    # path('replay/', views.replay, name='replay'),
    # path('watch/<path:file_path>', views.watch_video, name='watch_video'),
]