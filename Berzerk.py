"""
    File name: Berzerk.py
    Language: Python 2.x
    Aurhor Name: Devavrat Kalam
    Description: Implementing three agents to play Berzerk game.
"""


from __future__ import division
import argparse
from gym import wrappers, logger
import time
import gym
import csv
from agent1 import *
from agent2 import *


class randomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        # Do random moves
        tempAction = self.action_space.sample()
        return tempAction


# Random agent call
def randomAgentCall(agent, iterations):
    episode_count = iterations
    t11 = time.time()

    # Log files
    totalScore = []
    totallevels_crossed = []
    totalEnemyKills = []
    totaltimeTaken = []
    level = 1

    for epi in range(episode_count):
        # Resetting the environment
        tStart = time.time()
        reward = 0
        score = 0
        enemyKills = 0
        done = False
        # Max steps taken in 1 episode. This is set as sometimes, agent might get stuck
        max_iterations = 1000
        ob = env.reset()

        while not done and max_iterations > 0:
            action = agent.act(ob, reward, done)
            ob, reward, done, x = env.step(action)

            # Values are modified and recorded
            if reward == 50:
                # 50 points reward is for killing enemies
                enemyKills += 1
            score += reward
            max_iterations -= 1
            env.render()

            # Increase or comment sleep according to your preference
            time.sleep(0.01)

        # Recording progress
        totalScore.append(score)
        totallevels_crossed.append(level)
        totalEnemyKills.append(enemyKills)
        totaltimeTaken.append(round(time.time() - tStart, 2))

    t12 = time.time()
    difference = t12 - t11

    # Printing progess
    printingStats(totalScore, totallevels_crossed, totalEnemyKills, totaltimeTaken, episode_count, difference)

    # Storing the values into respective csv file
    with open("randomAData.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])


# My agent 1 call
def myAgent1Call(agent, iterations):
    episode_count = iterations
    t11 = time.time()

    # Log files
    totalScore = []
    totallevels_crossed = []
    totalEnemyKills = []
    totaltimeTaken = []

    for epi in range(episode_count):
        # Resetting the environment
        tStart = time.time()
        score = 0
        level = 0
        enemyKills = 0
        done = False
        # Max steps taken in 1 episode. This is set as sometimes, agent might get stuck
        max_iterations = 2000
        ob = env.reset()

        # Resetting Agent's class variables
        agent.level = 0
        agent.blackout = True
        agent.bscreen = False
        agent.innerRewards = 0
        agent.enemyKills = 0
        while not done and max_iterations > 0:
            action = agent.act(ob)
            ob, reward, done, x = env.step(action)

            # Values are modified and recorded
            if reward == 50:
                # 50 points reward is for killing enemies
                enemyKills += 1
            score += reward
            max_iterations -= 1
            env.render()

            # Increase or comment sleep according to your preference
            time.sleep(0.02)

        # Modifying the answers with agent's inner action records
        level += agent.level
        score += agent.innerRewards

        # Removing approx 1 enemy count as sometimes score board gives 50 points extra for killing all enemies or
        # travelling to another room
        enemyKills += agent.enemyKills - 1

        # recording progress
        totalScore.append(score)
        totallevels_crossed.append(level)
        totalEnemyKills.append(enemyKills)
        totaltimeTaken.append(round(time.time() - tStart, 2))

    t12 = time.time()
    difference = t12 - t11

    # Printing progess
    printingStats(totalScore, totallevels_crossed, totalEnemyKills, totaltimeTaken, episode_count, difference)

    # Storing the values into respective csv file
    with open("Agent1Data.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])


# My Agent 2 call
def myAgent2Call(agent, iterations):
    episode_count = iterations
    t11 = time.time()

    # Log files
    totalScore = []
    totallevels_crossed = []
    totalEnemyKills = []
    totaltimeTaken = []

    for epi in range(episode_count):
        # Resetting the environment
        tStart = time.time()
        score = 0
        level = 0
        enemyKills = 0
        done = False
        # Max steps taken in 1 episode. This is set as sometimes, agent might get stuck
        max_iterations = 2000
        ob = env.reset()

        # Resetting Agent's class variables
        agent.level = 0
        agent.blackout = True
        agent.bscreen = False
        agent.innerRewards = 0
        agent.enemyKills = 0
        while not done and max_iterations > 0:
            action = agent.act(ob)
            ob, reward, done, x = env.step(action)

            # Values are modified and recorded
            if reward == 50:
                # 50 points reward is for killing enemies
                enemyKills += 1
            score += reward
            max_iterations -= 1
            env.render()

            # Increase or comment sleep according to your preference
            time.sleep(0.02)

        # Modifying the answers with agent's inner action records
        level += agent.level
        score += agent.innerRewards

        # Removing approx 1 enemy count as sometimes score board gives 50 points extra for killing all enemies or
        # travelling to another room
        enemyKills += agent.enemyKills - 1

        # recording progress
        totalScore.append(score)
        totallevels_crossed.append(level)
        totalEnemyKills.append(enemyKills)
        totaltimeTaken.append(round(time.time() - tStart, 2))

    t12 = time.time()
    difference = t12 - t11

    # Printing progess
    printingStats(totalScore, totallevels_crossed, totalEnemyKills, totaltimeTaken, episode_count, difference)

    # Storing the values into respective csv file
    with open("Agent2Data.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])


def printingStats(totalScore, totallevels_crossed, totalEnemyKills, totaltimeTaken, episode_count, difference):
    # Printing progess
    print "Scores = ", totalScore
    print "Levels crossed = ", totallevels_crossed
    print "Enemies killed = ", totalEnemyKills
    print "Time taken in seconds = ", totaltimeTaken
    print "Maximum score obtained = ", max(totalScore)
    print "Total time for {} episodes in seconds = {}".format(episode_count, round(difference, 2))
    print "Total time for {} episodes in minutes = {}".format(episode_count, round((difference) / 60, 2))
    print "Mean time per episode = ", round(sum(totaltimeTaken) / episode_count, 2)
    print "Mean score per episode = ", round(sum(totalScore) / episode_count, 2)


def main():
    print
    print "----------------------------------------------------------------------------"
    print "Random Agent's stats -"
    print
    agent = randomAgent(env.action_space)
    special_data = {}
    special_data['ale.lives'] = 3

    # Random agent
    randomAgentCall(agent, numOfEpisodes)

    print
    print "----------------------------------------------------------------------------"
    print "My Agent1's stats -"
    print
    agent = Agent1(env)
    special_data = {}
    special_data['ale.lives'] = 3

    # My first agent
    myAgent1Call(agent, numOfEpisodes)

    print
    print "----------------------------------------------------------------------------"
    print "My Agent2's stats -"
    print
    agent = Agent2(env)
    special_data = {}
    special_data['ale.lives'] = 3

    # My first agent
    myAgent2Call(agent, numOfEpisodes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()
    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)
    env = gym.make(args.env_id)
    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'
    env.seed(0)

    # Define how many number of episode agents should perform
    numOfEpisodes = 3

    # Main function call
    main()

    env.close()