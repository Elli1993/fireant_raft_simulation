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
        self.attached = True
        self.index = index
        self.edgeDetected = False

        return;

    def randomwalk(self, env):
        """
        One step of a non-attached ant. It walks randomly and connects to the raft if it reaches an edge with a
        certain probability.
            """

        if (self.edgeDetected):
            self.findAttachment(env)
        else:
            x = randint(0, 3)
            self.moveAnt(x, env)
            self.randomwalk(env)

        return;

    def checkAttach(self, env, probability):
        """
        One step of an attached ant. It checks if it should let go and start a random walk.
        """
        index = [0, 1]
        var = [-1, 1]
        friends = 0
        print( 'starting pos ', self.position)
        if (self.attached):
            if (env[self.position[0], self.position[1], self.position[2] + 1] == 0):
                for v in var:
                    if (env[self.position[0] + v, self.position[1], self.position[2]] != 0):
                        friends += 1
                    if (env[self.position[0], self.position[1] + v, self.position[2]] != 0):
                        friends += 1
                #print("friends:", friends)
                if friends < 3 and random.uniform(0, 1) < probability:
                    # start randomwalk by doing a first step up and then to one side
                    print('walking starts')
                    self.position[2] += 1
                    #print('Current position: ', self.position)
                    x = randint(0, 3)
                    self.moveAnt(x, env,0.3)
                    self.randomwalk(env)
        print('end pos ', self.position)
        return;

    def getPosition(self):
        x = self.position
        return x;

    def findAttachment(self, env):
        """ moves downwards until finds a place to attach itself and attaches itself there
        """
        self.position[2] -= 1
        #print('find attach Current position: ', self.position)
        hasFriend = self.findFriends(env)
        while env[self.position[0], self.position[1], self.position[2] - 1] == 0 and hasFriend:
            self.position[2] -= 1
            #print('find attach Current position: ', self.position)
            if (self.findFriends(env) == False):
                hasFriend = False

        if hasFriend == False:
            self.position[2] += 1
            #print('find attach Current position: ', self.position)
            self.attached = True
            print('find attach ant attached again')
        elif env[self.position[0], self.position[1], self.position[2] - 1] == 0:
            self.attached = True
            print('find attach ant attached again')
        return;

    def findFriends(self, env):
        """ looks in x and y direction. if it finds other ants returns true if not returns false
        """
        var = [-1, 1]
        #print('looking for friends')
        for v in var:
            if (env[self.position[0] + v, self.position[1], self.position[2]] != 0 or env[
                self.position[0], self.position[1] + v, self.position[2]] != 0):
                return True

        return False

    def checkboundaries(self, env, position=[0, 0, 0]):
        if all(np.asarray(position) < env.shape):
            return True;
        else:
            return False;
        return;

    def checkOccupied(self, env, position=[0, 0, 0]):
        if env[position[0], position[1], position[2]] != 0:
            return False;
        return True;

    def checkEdgeDetected(self, env):
        if (env[self.position[0], self.position[1], self.position[2] - 1] == 0):
            return True;
        return False;

    def moveAnt(self, randNum, env, probability = 1.0):
        """
        moves ant in the direction the randNum indicates, 0:x+1, 1:x-1, 2:y+1, 3: y-1, if position is free
        if doesn't have an ant below -> edgeDetected=True
        """
        print('movingAnt', randNum)
        if randNum == 0:
            if (self.checkboundaries(env, (self.position[0] + 1, self.position[1], self.position[2]))):
                if (self.checkOccupied(env, (self.position[0] + 1, self.position[1], self.position[2]))):
                    self.position[0] += 1
                    if(self.checkEdgeDetected(env) and random.uniform(0,1) < probability):
                        self.edgeDetected = True
                    elif self.checkEdgeDetected(env) and random.uniform(0,1)>probability:
                        self.position[0]-=1
                        randNum=randint(0,3)
                        self.moveAnt(randNum,env)
                    print('move Current position: ', self.position)
            else:
                randNum = randint(0, 3)
                self.moveAnt(randNum,env)


        elif randNum == 1:
            if (self.checkboundaries(env, (self.position[0] + 1, self.position[1], self.position[2]))):
                if (self.checkOccupied(env, (self.position[0] - 1, self.position[1], self.position[2]))):
                    self.position[0] -= 1
                    if (self.checkEdgeDetected(env) and random.uniform(0, 1) < probability):
                        self.edgeDetected = True
                    elif self.checkEdgeDetected(env) and random.uniform(0, 1) > probability:
                        self.position[0] += 1
                        randNum = randint(0, 3)
                        self.moveAnt(randNum, env)
                    print('move Current position: ', self.position)
            else:
                randNum = randint(0, 3)
                self.moveAnt(randNum, env)

        elif randNum == 2:
            if (self.checkboundaries(env, (self.position[0] + 1, self.position[1], self.position[2]))):
                if (self.checkOccupied(env, (self.position[0], self.position[1] + 1, self.position[2]))):
                    self.position[1] += 1
                    if (self.checkEdgeDetected(env) and random.uniform(0, 1) < probability):
                        self.edgeDetected = True
                    elif self.checkEdgeDetected(env) and random.uniform(0, 1) > probability:
                        self.position[1] -= 1
                        randNum = randint(0, 3)
                        self.moveAnt(randNum, env)
                    print('move Current position: ', self.position)
            else:
                randNum = randint(0, 3)
                self.moveAnt(randNum, env)

        else:
            if (self.checkboundaries(env, (self.position[0] + 1, self.position[1], self.position[2]))):
                if (self.checkOccupied(env, (self.position[0], self.position[1] - 1, self.position[2]))):
                    self.position[0] -= 1
                    if (self.checkEdgeDetected(env) and random.uniform(0, 1) < probability):
                        self.edgeDetected = True
                    elif self.checkEdgeDetected(env) and random.uniform(0, 1) > probability:
                        self.position[1] += 1
                        randNum = randint(0, 3)
                        self.moveAnt(randNum, env)
                    print('move Current position: ', self.position)
            else:
                randNum = randint(0, 3)
                self.moveAnt(randNum, env)

        return;





