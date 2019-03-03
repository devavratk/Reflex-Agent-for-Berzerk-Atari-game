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
import numpy as np
import random
import csv


class randomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        # Do random moves
        tempAction = self.action_space.sample()
        return tempAction


class Agent1(object):
    """My best agent!"""
    def __init__(self):
        self.move = 2
        self.level = 0
        self.innerRewards = 0
        self.blackout = True
        self.bscreen = False
        self.enemyKills = 0

    def modifyRewardEnemy(self, reward):
        self.innerRewards += reward
        if reward == 50:
            self.enemyKills += 1

    # You should modify this function
    def act(self, observation):
        # Detecting Man pixel coordinates
        x, y, z = np.where(observation == 240)
        man = list(zip(x, y))

        # Detecting Wall pixel coordinates
        x, y, z = np.where(observation == 84)
        wall = dict(zip(list(zip(x,y)), [True] * len(x)))

        # Detecting Robots pixel coordinates
        x, y = np.where((np.invert(np.in1d(observation,[[0,0,0], [232,232,232],[240,240,240],[84,84,84]])).reshape(observation.shape)).all(2))
        robot = dict(zip(list(zip(x, y)), [True] * len(list(zip(x, y)))))

        # This condition deals with recoding levels changed during game
        if len(man) == 0:
            self.bscreen = True
        else:
            self.bscreen = False
            self.blackout = True
        if self.blackout and self.bscreen:
            self.level += 1
            self.blackout = False

        # If man is not yet on the screen, stay stationary
        if len(man) == 0:
            return 0

        # # Monsters Detection -
        # Man's middle Y coordinate
        middleY = man[len(man)//2][1]

        # Upper monster
        for i in range(man[0][0], 0, -1):
            if (i,middleY) in wall:
                break
            if (i,middleY) in robot:
                # Shoot
                ob, reward, done, x = env.step(10)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(3)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 10

        # Down monster
        for i in range(man[-1][0], 210):
            if (i,middleY) in wall:
                break
            if (i,middleY) in robot:
                # Shoot
                ob, reward, done, x = env.step(13)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(3)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 13

        # Man's middle X coordinate
        middleX = man[len(man)//2][0]

        # Left monster
        for i in range(man[0][1], 0, -1):
            if (middleX, i) in wall:
                break
            if (middleX, i) in robot:
                # Shoot
                ob, reward, done, x = env.step(12)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(5)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 12

        # Right monster
        for i in range(man[-1][1], 160):
            if (middleX, i) in wall:
                break
            if (middleX, i) in robot:
                # Shoot
                ob, reward, done, x = env.step(11)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(5)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 11

        # Considered possible moves Moves
        go = {2:"UP", 3:"RIGHT", 4:"LEFT", 5:"DOWN"}

        # Detect and avoid Bullets or robot from above and below
        try:
            for i in range(man[0][1] - 6, man[-1][1] + 6):
                for j in range(8):
                    if (man[0][0]-j, i) in robot or (man[0][0]-j, i) in wall:
                        del(go[2])
                    if (man[-1][0]+j, i) in robot or (man[-1][0]+j, i) in wall:
                        del(go[5])
        except:
            pass

        # Detect and avoid Bullets or robot from left and right
        try:
            for i in range(man[0][0] - 6, man[-1][0] + 6):
                for j in range(8):
                    if (i, man[0][1] - j) in robot:
                        del(go[4])
                    if (i, man[-1][1] + j) in robot:
                        del(go[3])
        except:
            pass

        # # Wall Detection
        # Upper wall
        if 2 in go:
            if (man[0][0]-8, man[0][1]) in wall or (man[0][0]-8, man[-1][1]) in wall\
                    or (man[0][0]-8, man[0][1]) in robot or (man[0][0]-8, man[-1][1]) in robot:
                del(go[2])

        # Left side wall
        if 4 in go:
            if (man[0][0], man[0][1]-8) in wall or (man[-1][0], man[0][1]-8) in wall\
                    or (man[0][0], man[0][1]-8) in robot or (man[-1][0], man[0][1]-8) in robot:
                del (go[4])

        # Right side wall
        if 3 in go:
            if (man[0][0], man[-1][1]+8) in wall or (man[-1][0], man[-1][1]+8) in wall\
                    or (man[0][0], man[-1][1]+8) in robot or (man[-1][0], man[-1][1]+8) in robot:
                del(go[3])

        # Down wall
        if 5 in go:
            if (man[-1][0]+8, man[0][1]) in wall or (man[-1][0]+8, man[-1][1]) in wall\
                    or (man[-1][0]+8, man[0][1]) in robot or (man[-1][0]+8, man[-1][1]) in robot:
                del(go[5])

        # For exit in upper direction
        if self.move == 3 and (2 in go) and (5 in go):
            self.move = 2

        # If there are no possible directions to move, stay still
        if len(go) == 0:
            return 0

        # If old move is not possible in current environment
        if self.move not in go:
            self.move = random.choice(go.keys())

        # Return move
        return self.move


class Agent2(object):
    """My second best agent!"""
    def __init__(self):
        self.move = 2
        self.level = 0
        self.innerRewards = 0
        self.blackout = True
        self.bscreen = False
        self.enemyKills = 0

    def modifyRewardEnemy(self, reward):
        self.innerRewards += reward
        if reward == 50:
            self.enemyKills += 1

    # You should modify this function
    def act(self, observation):
        # Detecting Man pixel coordinates
        x, y, z = np.where(observation == 240)
        man = list(zip(x, y))

        # Detecting Wall pixel coordinates
        x, y, z = np.where(observation == 84)
        wall = dict(zip(list(zip(x, y)), [True] * len(x)))

        # Detecting Robots pixel coordinates
        x, y = np.where((np.invert(
            np.in1d(observation, [[0, 0, 0], [232, 232, 232], [240, 240, 240], [84, 84, 84]])).reshape(
            observation.shape)).all(2))
        robot = dict(zip(list(zip(x, y)), [True] * len(list(zip(x, y)))))

        # This condition deals with recoding levels changed during game
        if len(man) == 0:
            self.bscreen = True
        else:
            self.bscreen = False
            self.blackout = True
        if self.blackout and self.bscreen:
            self.level += 1
            self.blackout = False

        # If man is not yet on the screen, stay stationary
        if len(man) == 0:
            return 0

        # # Monsters Detection -
        # Man's middle Y coordinate
        middleY = man[len(man) // 2][1]

        # Upper monster
        for i in range(man[0][0], 0, -1):
            if (i, middleY) in wall:
                break
            if (i, middleY) in robot:
                # Shoot
                ob, reward, done, x = env.step(10)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(3)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 10

        # Down monster
        for i in range(man[-1][0], 210):
            if (i, middleY) in wall:
                break
            if (i, middleY) in robot:
                # Shoot
                ob, reward, done, x = env.step(13)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(3)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 13

        # Man's middle X coordinate
        middleX = man[len(man) // 2][0]

        # Left monster
        for i in range(man[0][1], 0, -1):
            if (middleX, i) in wall:
                break
            if (middleX, i) in robot:
                # Shoot
                ob, reward, done, x = env.step(12)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(5)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 12

        # Right monster
        for i in range(man[-1][1], 160):
            if (middleX, i) in wall:
                break
            if (middleX, i) in robot:
                # Shoot
                ob, reward, done, x = env.step(11)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = env.step(5)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 11

        # Considered possible moves Moves
        go = {2: "UP", 3: "RIGHT", 4: "LEFT", 5: "DOWN"}

        # # Wall Detection
        # Upper wall
        if (man[0][0] - 5, man[0][1]) in wall or (man[0][0] - 5, man[-1][1]) in wall \
                or (man[0][0] - 5, man[0][1]) in robot or (man[0][0] - 5, man[-1][1]) in robot:
            del (go[2])

        # Left side wall
        if (man[0][0], man[0][1] - 5) in wall or (man[-1][0], man[0][1] - 5) in wall \
                or (man[0][0], man[0][1] - 5) in robot or (man[-1][0], man[0][1] - 5) in robot:
            del (go[4])

        # Right side wall
        if (man[0][0], man[-1][1] + 5) in wall or (man[-1][0], man[-1][1] + 5) in wall \
                or (man[0][0], man[-1][1] + 5) in robot or (man[-1][0], man[-1][1] + 5) in robot:
            del (go[3])

        # Down wall
        if (man[-1][0] + 5, man[0][1]) in wall or (man[-1][0] + 5, man[-1][1]) in wall \
                or (man[-1][0] + 5, man[0][1]) in robot or (man[-1][0] + 5, man[-1][1]) in robot:
            del (go[5])

        # For exit in upper direction only when everyone is dead
        if len(robot) == 0:
            if self.move == 3 and (2 in go) and (5 in go):
                self.move = 2

        # If there are no possible directions to move, stay still
        if len(go) == 0:
            return 0

        # If old move is not possible in current environment
        if self.move not in go:
            self.move = random.choice(go.keys())

        # Return move
        return self.move


# Random agent call
def randomAgentCall(iterations):
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

    # Printing progess
    print "Scores = ", totalScore
    print "Levels crossed = ", totallevels_crossed
    print "Enemies killed = ", totalEnemyKills
    print "Time taken in seconds = ", totaltimeTaken
    print "Maximum score obtained = ", max(totalScore)
    print "Total time for {} episodes in seconds = {}".format(episode_count, round(t12 - t11, 2))
    print "Total time for {} episodes in minutes = {}".format(episode_count, round((t12 - t11) / 60, 2))
    print "Mean time per episode = ", round(sum(totaltimeTaken) / episode_count, 2)
    print "Mean score per episode = ", round(sum(totalScore) / episode_count, 2)

    # Storing the values into respective csv file
    with open("randomAData.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])


# My agent 1 call
def myAgent1Call(iterations):
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

    # Printing progess
    print "Scores = ", totalScore
    print "Levels crossed = ", totallevels_crossed
    print "Enemies killed = ", totalEnemyKills
    print "Time taken in seconds = ", totaltimeTaken
    print "Maximum score obtained = ", max(totalScore)
    print "Total time for {} episodes in seconds = {}".format(episode_count, round(t12 - t11, 2))
    print "Total time for {} episodes in minutes = {}".format(episode_count, round((t12 - t11) / 60, 2))
    print "Mean time per episode = ", round(sum(totaltimeTaken) / episode_count, 2)
    print "Mean score per episode = ", round(sum(totalScore) / episode_count, 2)

    # Storing the values into respective csv file
    with open("Agent1Data.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])
    myfile.close()


# My Agent 2 call
def myAgent2Call(iterations):
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

    # Printing progess
    print "Scores = ", totalScore
    print "Levels crossed = ", totallevels_crossed
    print "Enemies killed = ", totalEnemyKills
    print "Time taken in seconds = ", totaltimeTaken
    print "Maximum score obtained = ", max(totalScore)
    print "Total time for {} episodes in seconds = {}".format(episode_count, round(t12 - t11, 2))
    print "Total time for {} episodes in minutes = {}".format(episode_count, round((t12 - t11) / 60, 2))
    print "Mean time per episode = ", round(sum(totaltimeTaken) / episode_count, 2)
    print "Mean score per episode = ", round(sum(totalScore) / episode_count, 2)

    # Storing the values into respective csv file
    with open("Agent2Data.csv", "w") as myfile:
        writerF = csv.writer(myfile)
        fields = ["TotalScore", "TotalLevelsCrossed", "TotalEnemiesKilled", "TotalTimeRequired"]
        writerF.writerow(fields)
        for i in range(len(totalScore)):
            writerF.writerow([totalScore[i], totallevels_crossed[i], totalEnemyKills[i], totaltimeTaken[i]])
    myfile.close()


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
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


    print
    print "----------------------------------------------------------------------------"
    print "Random Agent's stats -"
    print
    agent = randomAgent(env.action_space)
    special_data = {}
    special_data['ale.lives'] = 3
    # Random agent
    randomAgentCall(numOfEpisodes)

    print
    print "----------------------------------------------------------------------------"
    print "My Agent1's stats -"
    print
    agent = Agent1()
    special_data = {}
    special_data['ale.lives'] = 3
    # My first agent
    myAgent1Call(numOfEpisodes)

    print
    print "----------------------------------------------------------------------------"
    print "My Agent2's stats -"
    print
    agent = Agent2()
    special_data = {}
    special_data['ale.lives'] = 3
    # My first agent
    myAgent2Call(numOfEpisodes)

    env.close()