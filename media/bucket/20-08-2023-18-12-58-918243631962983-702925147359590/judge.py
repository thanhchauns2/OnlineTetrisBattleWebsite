print('Hello!')
import sys
import agent1
import agent2
agent1 = agent1.Agent.Agent('')
agent2 = agent2.Agent.Agent('')
sys.path.append('D:\OnlineTetrisBattle-web')
from VideoRender import VideoRender
videorender =  VideoRender()
videorender.render(agent1=agent1, agent2=agent2, link='media/bucket/20-08-2023-18-12-58-918243631962983-702925147359590\\outpy.webm', fps=24)
