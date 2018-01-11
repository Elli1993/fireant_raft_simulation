# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:17:52 2018

"""

import numpy as np
import os
import random
from random import randint


class ant(object):
    '''
    Object simulating a single ant that can interact with the environment.
    Ants have self.position giving their current position in the environment and self.attached indicating if they
    are currently attached to the raft.
    '''

    def __init__(self, position=[0, 0, 0], index=0):
        """
        Initialize the ant and position it in the environment.
        Args:
            position: int array giving the initial position of the ant.
            """
        self.position = position
        self.attached = False
        self.index = index
        self.edgeDetected = False

        return;

    def randomwalk(self, env):
        """
        One step of a non-attached ant. It walks randomly and connects to the raft if it reaches an edge with a
        certain probability.
            """
        x = randint(0, 3)
        moveAnt(self, x, env)
        if (self.edgeDetected):
            findAttachment(self, env)
        else:
            randomwalk(self, env)

        return;

    def checkAttach(self, env, probability):
        """
        One step of an attached ant. It checks if it should let go and start a random walk.
        """
        index = [0, 1]
        var = [-1, 1]
        friends = 0
        if (self.attached):
            if (env[self.position[0]][self.position[1]][self.position[2] + 1] == 0):
                for v in var:
                    if (env[self.position[0] + var][self.position[1]][self.position[2]] != 0):
                        friends += 1
                    if (env[self.position[0]][self.position[1] + var][self.position[2]] != 0):
                        friends += 1

                if friends > 3 and random.uniform(0, 1) < probability:
                    # start randomwalk by doing a first step up and then to one side
                    self.position[2] += 1
                    x = randint(0, 3)
                    moveAnt(self, x, env)

        return;

    def moveAnt(self, randNum, env):
        """
        moves ant in the direction the randNum indicates, 0:x+1, 1:x-1, 2:y+1, 3: y-1, if position is free
        if doesn't have an ant below -> edgeDetected=True
        """
        # TODO: check if position is free

        if randNum == 0:
            if (env[self.position[0] + 1][self.position[1]][self.position[2]] == 0):
                self.position[0] += 1
                if (env[self.position[0]][self.position[1]][self.position[2] - 1] == 0):
                    self.edgeDetected = True
            else:
                randNum = randint(0, 3)


        elif randNum == 1:
            if (env[self.position[0] - 1][self.position[1]][self.position[2]] == 0):
                self.position[0] -= 1
                if (env[self.position[0]][self.position[1]][self.position[2] - 1] == 0):
                    self.edgeDetected = True
            else:
                randNum = randint(0, 3)

        elif randNum == 2:
            if (env[self.position[0]][self.position[1] + 1][self.position[2]] == 0):
                self.position[1] += 1
                if (env[self.position[0]][self.position[1]][self.position[2] - 1] == 0):
                    self.edgeDetected = True
            else:
                randNum = randint(0, 3)

        else:
            if (env[self.position[0]][self.position[1] - 1][self.position[2]] == 0):
                self.position[1] -= 1
                if (env[self.position[0]][self.position[1]][self.position[2] - 1] == 0):
                    self.edgeDetected = True
            else:
                randNum = randint(0, 3)

        return;

    def findAttachment(self, env):
        """ moves downwards until finds a place to attach itself and attaches itself there
        """
        self.position[2] -= 1
        hasFriend = findFriends
        while env[self.position[0]][self.position[1]][self.position[2] - 1] == 0 and hasFriend:
            self.position[2] -= 1
            if (findFriends(self, env) == False):
                hasFriend = False

        if hasFriend == False:
            self.position[2] += 1
            self.attached
        elif env[self.position[0]][self.position[1]][self.position[2] - 1] == 0:
            self.attached

        return;

    def findFriends(self, env):
        """ looks in x and y direction. if it finds other ants returns true if not returns false
        """
        var = [-1, 1]

        for v in var:
            if (env[self.position[0] + var][self.position[1]][self.position[2]] != 0 or
                        env[self.position[0]][self.position[1] + var][self.position[2]] != 0):
                return True

        return False
