print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent()
agent2 = agent2.Agent.Agent()
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/51242f75-9e39-4573-8f0d-5e4fbdb05f6a\\outpy.webm', fps=24)
