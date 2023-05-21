print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent()
agent2 = agent2.Agent.Agent()
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/572ea6d6-d7a0-420a-930e-1e75a3a2cf9e\\outpy.webm', fps=24)
