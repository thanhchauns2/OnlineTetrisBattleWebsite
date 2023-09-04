print('Hello!')
import sys
import agent1.Agent
import agent2.Agent
print('Agent 1:')
agent1 = agent1.Agent.Agent('')
print('Agent 2:')
agent2 = agent2.Agent.Agent('')
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/20-08-2023-18-18-17-702925147359590-918243631962983\\outpy.webm', fps=24)
