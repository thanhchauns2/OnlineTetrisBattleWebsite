print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
agent1 = agent1.Agent.Agent()
agent2 = agent2.Agent.Agent()
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/28-06-2023-16-57-25-540768866129950-790034239892761\\outpy.webm', fps=100)
