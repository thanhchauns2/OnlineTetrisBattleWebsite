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

def breed(a, b):
    lines = random.random()
    if lines < 0.45:
        lines = a.LINES_POINTS
    elif lines < 0.9:
        lines = b.LINES_POINTS
    else:
        lines = random.uniform(0, 1)
    
    holes = random.random()
    if holes < 0.45:
        holes = a.HOLES_POINTS
    elif holes < 0.9:
        holes = b.HOLES_POINTS
    else:
        holes = random.uniform(-1, 0)
    
    height = random.random()
    if height < 0.45:
        height = a.HEIGHT_POINTS
    elif height < 0.9:
        height = b.HEIGHT_POINTS
    else:
        height = random.uniform(-1, 0)
    
    bumpiness = random.random()
    if bumpiness < 0.45:
        bumpiness = a.BUMPINESS_POINTS
    elif bumpiness < 0.9:
        bumpiness = b.BUMPINESS_POINTS
    else:
        bumpiness = random.uniform(-1, 0)
    
    return Agent(lines = lines,
                  holes = holes,
                  height = height,
                  bumpiness= bumpiness)

def duel(a, b):

    env = TetrisDoubleEnv(gridchoice="none", obs_type="grid", mode="rgb_array")

    done = False
    state = env.reset()
    agent_list = [a, b]
    # imgs = []

    while not done:
        img = env.render(mode='rgb_array')
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # imgs.append(img)
        action = agent_list[env.game_interface.getCurrentPlayerID()].choose_action(state)
        state, reward, done, _ = env.step(action)
        env.take_turns()
        # cv2.imshow('image', img)
        # cv2.waitKey(2)
    
    # cv2.destroyAllWindows()
    return _['winner']

def selection(pool):
    pool_sorted = sorted(pool, key=lambda x: x[1], reverse=True)

    df = pd.read_csv('filename.csv', header=None)
    best_selection = df.values[1][1:]

    new_pool = pool_sorted[:POPULATION // 10]

    while len(new_pool) < POPULATION:
        x = random.randint(0, POPULATION // 2)
        y = random.randint(0, POPULATION // 2)
        new_pool.append([breed(pool_sorted[x][0], pool_sorted[y][0]), 0])
    
    for i in new_pool:
        i[1] = 0

    return new_pool


def main():
    # pool = [[create_agent(), 0] for i in range(POPULATION)]
    pool = []
    df = pd.read_csv('genetics.csv', header=None)
    # best_selection = df.values[1:][1:]
    best_selection = [x[1:] for x in df.values[1:]]
    for i in range(len(best_selection)):
        pool.append([Agent(
            lines = best_selection[i][0],
            holes = best_selection[i][1],
            height = best_selection[i][2],
            bumpiness= best_selection[i][3],
        ), 0])
    for epoch in range(EPOCHS):
        for x in range(POPULATION):
            for y in range(x + 1, POPULATION):
                print(pool[x][0].LINES_POINTS, pool[x][0].HOLES_POINTS, pool[x][0].BUMPINESS_POINTS, pool[x][0].HEIGHT_POINTS)
                print(pool[y][0].LINES_POINTS, pool[y][0].HOLES_POINTS, pool[y][0].BUMPINESS_POINTS, pool[y][0].HEIGHT_POINTS)
                results = duel(pool[x][0], pool[y][0])
                if results == 0:
                    pool[x][1] += 1
                    pool[y][1] -= 0.5
                else:
                    pool[y][1] += 1
                    pool[x][1] -= 0.5
        pool = selection(pool)
    results = []
    for i in pool:
        # print(i[0].LINES_POINTS, i[0].HOLES_POINTS, i[0].BUMPINESS_POINTS, i[0].HEIGHT_POINTS)
        results.append([i[0].LINES_POINTS, i[0].HOLES_POINTS, i[0].BUMPINESS_POINTS, i[0].HEIGHT_POINTS])
    pd.DataFrame(results).to_csv("genetics.csv")

main()
