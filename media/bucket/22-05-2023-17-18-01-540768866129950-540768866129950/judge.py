print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent()
agent2 = agent2.Agent.Agent()
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/22-05-2023-17-18-01-540768866129950-540768866129950\\outpy.webm', fps=100)
