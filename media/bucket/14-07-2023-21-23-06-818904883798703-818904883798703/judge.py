print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent('')
agent2 = agent2.Agent.Agent('')
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/14-07-2023-21-23-06-818904883798703-818904883798703\\outpy.webm', fps=100)
