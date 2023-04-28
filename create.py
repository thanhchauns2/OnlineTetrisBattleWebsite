from TetrisBattle.envs.tetris_env import TetrisDoubleEnv
from CustomAgent import Agent
import random, pandas as pd, cv2

POPULATION = 20
EPOCHS = 5
BATTLES = 20

def create_agent():
    return Agent(lines = random.uniform(0, 1),
                  holes = random.uniform(-1, 0),
                  height = random.uniform(-1, 0),
                  bumpiness= random.uniform(-1, 0))

pool = [[create_agent(), 0] for i in range(POPULATION)]

results = []
for i in pool:
    results.append([i[0].LINES_POINTS, i[0].HOLES_POINTS, i[0].BUMPINESS_POINTS, i[0].HEIGHT_POINTS])
    print([i[0].LINES_POINTS, i[0].HOLES_POINTS, i[0].BUMPINESS_POINTS, i[0].HEIGHT_POINTS])
pd.DataFrame(results).to_csv("genetics.csv")

# df = pd.read_csv('genetics.csv', header=None)
# # best_selection = df.values[1:][1:]
# best_selection = [x[1:] for x in df.values[1:]]
# print(best_selection)
# for i in range(len(best_selection)):
#     print(best_selection[i][0], best_selection[i][1], best_selection[i][2], best_selection[i][3])