from TetrisBattle.envs.tetris_env import TetrisDoubleEnv
from CustomAgent import Agent
# from Agent import Test
import cv2, time, random
import numpy as np
import pandas as pd

class Agent2:
    def __init__(self) -> None:
        pass

    def choose_action(self, obs):
        return 0
        # return random.randint(3, 6)
        # return random.randint(0, 7)

env = TetrisDoubleEnv(gridchoice="none", obs_type="grid", mode="rgb_array")

genes = [[83.9582, 85.5775, 1.0495, 1.0602, 5.7449, 13.3834, 13.8588, 6.7820, 2.1385, -6.0317]]

done = False
state = env.reset()
agent_list = [
            Agent(0),
            Agent(1)
            ,]

imgs = []

while not done:
    img = env.render(mode='rgb_array') # img is rgb array, you need to render this or can check my colab notebook in readme file
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    imgs.append(img)
    action = agent_list[env.game_interface.getCurrentPlayerID()].choose_action(state)
    state, reward, done, _ = env.step(action)
    print(_)
    env.take_turns()
    cv2.imshow('image', img)
    cv2.imwrite('img.jpg',img)
    cv2.waitKey(2)

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc(*'DIVX'), 25, (800,600))
for img in imgs:
    out.write(img)
out.release()

cv2.destroyAllWindows()