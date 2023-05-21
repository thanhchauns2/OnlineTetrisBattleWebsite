print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent()
agent2 = agent2.Agent.Agent()
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/5b8e8dd9-fb07-4fc5-932d-6a9de49fd569\\outpy.webm', fps=24)
