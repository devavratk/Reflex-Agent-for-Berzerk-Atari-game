** Berzerk.py file information **

1) The code contains __name__ condition at the bottom which includes:
- Basic setup code for the game.
- "numOfEpisodes" named variable which determine how many episodes all 
  3 agents will play.
- Lines of code to call random agent
- Lines of code to call agent1
- Lines of code to call agent2

2) Three functions named "randomAgentCall", "myAgent1Call" and "myAgent2Call" which are called in sequence implementing their respective agents.
All functions take "numOfEpisodes" as argument.
These files are located in middle part of the code, just above __name__ condition.

3) Three agent classes "randomAgent", "Agent1" and "Agent2", consisting method called "act()" which is responsible to take actions whenever called from their respective functions.



** Implementation instructions **
- Change value of "numOfEpisodes" for changing number of episodes each agent will play.
- If you want to implement a specific agent, comment out the other agent call lines. 
  Agent call lines are -
  randomAgentCall(numOfEpisodes)
  and
  myAgent1Call(numOfEpisodes)
  and
  myAgent2Call(numOfEpisodes)
- A "time.sleep(0.01)" is included in every agent call function. You can manually change it to increase or decrease the speed of game to simplify visuals.
  This sleep can be found at lines -
  388 for random agent,
  459 for agent1,
  539 for agent 2.

IMPORTANT NOTE -
Enjoy the game
