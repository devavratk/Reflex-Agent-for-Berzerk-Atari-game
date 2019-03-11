import random
import numpy as np


class Agent2(object):
    """My second best agent!"""
    def __init__(self, env):
        self.env = env
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
                ob, reward, done, x = self.env.step(10)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = self.env.step(3)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 10

        # Down monster
        for i in range(man[-1][0], 210):
            if (i, middleY) in wall:
                break
            if (i, middleY) in robot:
                # Shoot
                ob, reward, done, x = self.env.step(13)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = self.env.step(3)
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
                ob, reward, done, x = self.env.step(12)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = self.env.step(5)
                self.modifyRewardEnemy(reward)

                # Shoot again
                return 12

        # Right monster
        for i in range(man[-1][1], 160):
            if (middleX, i) in wall:
                break
            if (middleX, i) in robot:
                # Shoot
                ob, reward, done, x = self.env.step(11)
                self.modifyRewardEnemy(reward)

                ob, reward, done, x = self.env.step(5)
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