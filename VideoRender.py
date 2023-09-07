from TetrisBattle.envs.tetris_env import TetrisDoubleEnv
from CustomAgent import Agent
import cv2
import numpy as np
import pandas as pd
from moviepy.editor import ImageSequenceClip
from moviepy.video.fx.resize import resize
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.editor import CompositeAudioClip
from moviepy.editor import afx
from moviepy.editor import AudioFileClip
from django.templatetags.static import static

class VideoRender():

    def __init__(self) -> None:
        pass

    def render(self, agent1, agent2, agent1_name=None, agent2_name=None, link = 'outpy.webm', fps = 200):
        
        agent_list = [agent1, agent2]
        env = TetrisDoubleEnv(gridchoice="none", obs_type="grid", mode="rgb_array")
        done = False
        state = env.reset(name1=agent1_name, name2=agent2_name)

        imgs = []

        while not done:
            img = env.render(mode='rgb_array') # img is rgb array, you need to render this or can check my colab notebook in readme file
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            imgs.append(img)
            action = agent_list[env.game_interface.getCurrentPlayerID()].choose_action(state)
            state, reward, done, _ = env.step(action)
            env.take_turns()
        
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc(*'DIVX'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('M', 'P', 'E', 'G'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('h', '2', '6', '4'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('X', '2', '6', '4'), fps, (800,600))
        # out = cv2.VideoWriter(link,cv2.VideoWriter_fourcc('V', 'P', '8', '0'), fps, (800,600))
        # for img in imgs:
        #     cv2.imwrite('img.jpg',img)
        #     out.write(img)
        # out.release()

        # out1 = ImageSequenceClip(imgs, fps=fps)
        # print('duration: ', out1.duration)
        # out1.write_videofile(link, fps=fps, bitrate='50000k')

        # print('number of frames: ', len(imgs))
        # data_audio = np.random.uniform(-1, 1, (len(imgs), 1))
        # data_audio = AudioArrayClip(data_audio, fps=fps)
        # data_audio = CompositeAudioClip([data_audio])

        data_audio = AudioFileClip('static/audio/battlemusicmp3.mp3')
        out = ImageSequenceClip(imgs, fps=fps)
        data_audio = afx.audio_loop(data_audio, duration=out.duration)
        out.audio = data_audio
        out = out.set_duration(out.duration)
        out.write_videofile(link, fps=fps, bitrate='50000k')

        with open(link[:-4] + 'txt', 'w') as file:
            file.write(str(_['winner']) + '\n')

        # cv2.destroyAllWindows()

        return link
