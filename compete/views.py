from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
import os
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from VideoRender import VideoRender
from CustomAgent import Agent as ag
import importlib
import uuid, sys
from .models import *
from .forms import *

@csrf_exempt
def prepare(request):
    return render(request, 'compete/prepare.html')

@csrf_exempt
def training(request):
    return render(request, 'compete/training.html')

@csrf_exempt
def competition(request):
    form = FileUploadForm()
    error_message = ''
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            file = form.cleaned_data['file']
            if file.name != 'agent.py':
                error_message = 'Invalid file type. Only agent.py is allowed.'
            else:
                
                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'compete', 'agent1')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.py'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'compete', 'agent2')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent2.py'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                error_message = 'Uploaded successfully.'

    return render(request, 'compete/competition.html', {'form': form, 'error_message': error_message})

@csrf_exempt
def single(request):
    form = FileUploadForm()
    error_message = ''
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            file = form.cleaned_data['file']
            if file.name != 'agent.py':
                error_message = 'Invalid file type. Only agent.py is allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'single', 'agent1')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.py'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return redirect('/compete/watch/?mode=single&player=' + str(user.id))

    return render(request, 'compete/training/single.html', {'form': form, 'error_message': error_message})

@csrf_exempt
def load_agents_single_player(path1, path2):
    temp_sys_path = sys.path[:] 
    sys.path.append(path1)
    sys.path.append(path2)
    from agent1 import Agent as agt1
    from agent import Agent as agt2
    agent1 = agt1()
    agent2 = agt2()
    sys.path = temp_sys_path  
    return agent1, agent2

@csrf_exempt
def duel(request):
    form = FileUploadDuelForm()
    error_message = ''
    if request.method == 'POST':
        form = FileUploadDuelForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            file = form.cleaned_data['file1']
            if file.name != 'agent1.py':
                error_message = 'Invalid file type. Only agent1.py and agent2.py are allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'duel', 'agent2')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.py'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            
            file = form.cleaned_data['file2']
            if file.name != 'agent2.py':
                error_message = 'Invalid file type. Only agent1.py and agent2.py are allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'duel', 'agent2')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent2.py'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return redirect('/compete/watch/?mode=duel&player=' + str(user.id))

    return render(request, 'compete/training/duel.html', {'form': form, 'error_message': error_message})

@csrf_exempt
def load_agents_duel(path1, path2):
    temp_sys_path = sys.path[:]
    sys.path.append(path1)
    sys.path.append(path2)
    from agent1 import Agent as agt1
    from agent2 import Agent as agt2
    agent1 = agt1()
    agent2 = agt2()
    sys.path = temp_sys_path 
    return agent1, agent2

@csrf_exempt
def watch(request):
    videorender = VideoRender()
    link = str(uuid.uuid4()) + ".mp4"
    # link = os.path.join('media', 'bucket', link)
    link = os.path.join('bucket', link)
    link = os.path.join(settings.MEDIA_ROOT, link)
    # print(link)
    # print(settings.MEDIA_ROOT)
    mode = request.GET.get('mode')
    # agent1 = ag()
    # agent2 = ag()
    if request.method == 'GET':
        if mode == 'single':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'single', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'all')
            agent1, agent2 = load_agents_single_player(link1, link2)
        elif mode == 'duel':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent2')
            agent1, agent2 = load_agents_duel(link1, link2)
        elif mode == 'compete':
            player1_id = request.GET.get('player1')
            player2_id = request.GET.get('player2')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player1_id, 'training', 'compete', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player2_id, 'training', 'compete', 'agent2')
            agent1, agent2 = load_agents_duel(link1, link2)
    link = link.replace('\\', '/')
    videorender.render(agent1=agent1, agent2=agent2, link=link, fps=24)
    print(link)
    context = {'link': link}
    return render(request, 'compete/watch.html', context=context)
