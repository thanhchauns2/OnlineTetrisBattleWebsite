import uuid, os, shutil, zipfile
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from django.conf import settings

def generate_game(link1, link2, link, player1_id, player2_id):
    # Copy 2 file zip vào link bucket
    zipfile1 = os.path.join(link, 'agent1.zip')
    zipfile2 = os.path.join(link, 'agent2.zip')
    shutil.copy(link1, zipfile1)
    shutil.copy(link2, zipfile2)
    with zipfile.ZipFile(zipfile1, 'r') as zip_ref:
        zip_ref.extractall(link)
    with zipfile.ZipFile(zipfile2, 'r') as zip_ref:
        zip_ref.extractall(link)
    
    file_path = os.path.join(link, 'judge.py')
    current_path = os.path.abspath('')
    video_path = os.path.join(link, 'outpy.webm')

    with open(file_path, 'w') as file:
        file.write('print(\'Hello!\')\n')
        file.write('import ' + str(player1_id) + '.agent\n')
        file.write('import ' + str(player2_id) + '.agent\n')
        file.write('agent1 = ' + str(player1_id) + '.agent.Agent()\n')
        file.write('agent2 = ' + str(player2_id) + '.agent.Agent()\n')
        file.write('sys.path.append(\'' + current_path + '\')\n')
        file.write('from VideoRender import VideoRender\n')
        file.write('videorender.render(agent1=agent1, agent2=agent2, link=\'' + video_path + '\', fps=24)\n')

    os.system('python3 ' + file_path)

    return video_path

@csrf_exempt
def watch(request):
    link = str(uuid.uuid4())
    # link = link + ".webm"
    link = os.path.join('media', 'bucket', link)
    # link = os.path.join('bucket', link)
    # link = os.path.join(settings.MEDIA_ROOT, link)
    link = link.replace('\\', '/')
    # link = os.path.abspath(link)
    print(os.path.abspath(link))
    mode = request.GET.get('mode')
    if request.method == 'GET':
        if mode == 'single':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'single', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'all', '0')
            player1_id = player_id
            player2_id = 0
        elif mode == 'duel':
            player_id = request.GET.get('player')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player_id, 'training', 'duel', 'agent2')
            player1_id = player_id
            player2_id = player_id
        elif mode == 'compete':
            player1_id = request.GET.get('player1')
            player2_id = request.GET.get('player2')
            link1 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player1_id, 'training', 'compete', 'agent1')
            link2 = os.path.join(settings.MEDIA_ROOT, 'pool', 'byid', player2_id, 'training', 'compete', 'agent2')
    link = generate_game(link1, link2, link, player1_id, player2_id)
    print(link)
    context = {'link': link}
    return render(request, 'compete/watch.html', context=context)
