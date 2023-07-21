import datetime, os, shutil, zipfile
from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from registration.models import UserProfile
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
    form = TournamentForm()
    error_message = 'Welcome to PTIT'
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            file = form.cleaned_data['file']
            if file.name != 'agent.zip':
                error_message = 'Invalid file type. Only agent.zip is allowed.'
            else:
                
                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'compete', 'agent1')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.zip'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'compete', 'agent2')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent2.zip'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                error_message = 'Uploaded successfully.'
        else:
            form = TournamentForm(request.POST)
            user = request.user
            # print(1120)
            if form.is_valid():
                # print(11)
                tournament_id = form.cleaned_data['tournament_id']
                user.userprofile.competition_id = int(tournament_id)
                user.userprofile.save()
                error_message = 'Uploaded tournament id.'

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
            if file.name != 'agent.zip':
                error_message = 'Invalid file type. Only agent.zip is allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'single', 'agent1')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.zip'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return redirect('/compete/watch/?mode=single&player=' + str(user.id))

    return render(request, 'compete/training/single.html', {'form': form, 'error_message': error_message})

@csrf_exempt
def duel(request):
    form = FileUploadDuelForm()
    error_message = ''
    if request.method == 'POST':
        form = FileUploadDuelForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            file = form.cleaned_data['file1']
            if file.name != 'agent1.zip':
                error_message = 'Invalid file type. Only agent1.zip is allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'duel', 'agent1')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent1.zip'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            
            file = form.cleaned_data['file2']
            if file.name != 'agent2.zip':
                error_message = 'Invalid file type. Only agent2.zip is allowed.'
            else:

                pool_path = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', str(user.id), 'training', 'duel', 'agent2')
                if not os.path.exists(pool_path):
                    os.makedirs(pool_path)
                file.name = 'agent2.zip'
                file_path = os.path.join(pool_path, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return redirect('/compete/watch/?mode=duel&player=' + str(user.id))

    return render(request, 'compete/training/duel.html', {'form': form, 'error_message': error_message})

def generate_game(link1, link2, link, player1_id, player2_id):
    # Copy 2 file zip vào link bucket
    zipfile1 = os.path.join(link, 'agent1.zip')
    zipfile2 = os.path.join(link, 'agent2.zip')
    shutil.copy(link1, zipfile1)
    shutil.copy(link2, zipfile2)
    with zipfile.ZipFile(zipfile1, 'r') as zip_ref:
        zip_ref.extractall(link)
        agentlink = os.path.join(link, 'agent')
        try:
            os.rename(agentlink, os.path.join(link, 'agent1').replace('\\', '/'))
        except:
            pass
    with zipfile.ZipFile(zipfile2, 'r') as zip_ref:
        zip_ref.extractall(link)
        agentlink = os.path.join(link, 'agent')
        try:
            os.rename(agentlink, os.path.join(link, 'agent2').replace('\\', '/'))
        except:
            pass
    
    file_path = os.path.join(link, 'judge.py')
    current_path = os.path.abspath('')
    video_path = os.path.join(link, 'outpy.webm')

    with open(file_path, 'w') as file:
        file.write('print(\'Hello!\')\n')
        file.write('import sys\n')
        file.write('import agent1.Agent\n')
        file.write('import agent2.Agent\n')
        file.write('agent1 = agent1.Agent.Agent(\'\')\n')
        file.write('agent2 = agent2.Agent.Agent(\'\')\n')
        file.write('sys.path.append(\'' + current_path + '\')\n')
        file.write('from VideoRender import VideoRender\n')
        file.write('videorender =  VideoRender()\n')
        file.write('videorender.render(agent1=agent1, agent2=agent2, link=\'' + video_path.replace('\\', '\\\\') + '\', fps=100)\n')

    os.system('python3 ' + file_path)

    return video_path

@csrf_exempt
def watch(request):
    mode = request.GET.get('mode')
    if request.method == 'GET':
        if mode == 'single':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'single', 'agent1', 'agent1.zip')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'all', '0', 'agent2', 'agent2.zip')
            player1_id = player_id
            player2_id = 0
            name_1 = 'Participant'
            name_2 = 'System'
        elif mode == 'duel':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent1', 'agent1.zip')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent2', 'agent2.zip')
            player1_id = player_id
            player2_id = player_id
            name_1 = 'Agent 1'
            name_2 = 'Agent 2'
        elif mode == 'compete':
            player1_id = request.GET.get('player1')
            player2_id = request.GET.get('player2')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player1_id, 'training', 'compete', 'agent1', 'agent1.zip')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player2_id, 'training', 'compete', 'agent2', 'agent2.zip')
            name_1 = User.objects.get(id=player1_id).username
            name_2 = User.objects.get(id=player2_id).username
    now = datetime.datetime.now()
    link = now.strftime("%d-%m-%Y-%H-%M-%S") + "-" + str(player1_id) + '-' + str(player2_id) 
    link = os.path.join('media', 'bucket', link)
    link = link.replace('\\', '/')
    if not os.path.exists(link):
        os.makedirs(link)
    video_link = generate_game(link1, link2, link, player1_id, player2_id)
    result_link = video_link[:-4] + 'txt'
    winner, id, name = 0, 0, 0
    message, message2 = "", ""
    try:
        with open(result_link, 'r') as file:
            content = file.read()
            if content[0] == '0':
                id = player1_id
                lose = player2_id
                winner = name_1
                loser = name_2
            else:
                id = player2_id
                lose = player1_id
                winner = name_2
                loser = name_1
            message = winner + " win!"
            if mode == 'compete':
                S1, S2, N1, N2 = calculate_elo(id_win=id, id_lose=lose)
                message2 = "New elo: {} {} -> {}, {} {} -> {}".format(winner, S1, N1, loser, S2, N2)
                
    except FileNotFoundError:
        print(f"File '{result_link}' not found.")
    context = {'link': video_link, 'message': message, 'message2' : message2}
    return render(request, 'compete/watch.html', context=context)

def calculate_elo(id_win, id_lose):
    user1 = User.objects.get(id=id_win)
    user2 = User.objects.get(id=id_lose)
    K1 = 10
    K2 = 10
    R1 = user1.userprofile.elo
    R2 = user2.userprofile.elo
    if R1 < 2400:
        K1 = 15
    elif R1 < 2000:
        K1 = 20
    elif R1 < 1600:
        K1 = 25
    if R2 < 2400:
        K2 = 15
    elif R2 < 2000:
        K2 = 20
    elif R2 < 1600:
        K2 = 25
    Q1 = 10 ** (R1 // 400)
    Q2 = 10 ** (R2 // 400)
    E1 = Q1 / (Q1 + Q2)
    E2 = Q2 / (Q1 + Q2)
    R1a = int(R1 + K1 * (1 - E1))
    R2a = int(R2 + K2 * (0 - E2))
    user1.userprofile.elo = R1a
    user1.userprofile.save()
    user2.userprofile.elo = R2a
    user2.userprofile.save()
    return (R1, R2, R1a, R2a)

@csrf_exempt
def tournament(request):
    error_message = ''
    if request.method == 'POST':
        if not request.POST.get('tournament_id'):
            tournament_id = request.POST.get('tournament_id')
            print(tournament_id)
            return redirect('/compete/tournament/?error_message={}&mode=compete&tournament_id={}'.format(
                error_message, tournament_id
            ))
        if not request.POST.get('ID1'):
            tournament_id = request.POST.get('tournament_id')
            print(tournament_id, 'None')
            return redirect('/compete/tournament/?error_message={}&mode=compete&tournament_id={}'.format(
                error_message, tournament_id
            ))
        if request.POST.get('tournament_id') != 'None':
            ID1 = request.POST.get('ID1')
            ID2 = request.POST.get('ID2')
            tournament_id = request.POST.get('tournament_id')
            print(tournament_id)
            return redirect('/compete/watch/?error_message={}&mode=compete&player1={}&player2={}&tournament_id={}'.format(
                error_message, ID1, ID2, tournament_id
            ))
    return render(request, 'compete/tournament.html', {'error_message': error_message, 'tournament_id' : None})