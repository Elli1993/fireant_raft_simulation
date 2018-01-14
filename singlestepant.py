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

    def getPosition(self):
        x = self.position
        return x;

    def findFriends(self, env):
        """
        looks in x and y direction. if it finds other ants returns true if not returns false
        Args:
            env: 3D int array showing the discrete environment.
        """
        var = [-1, 1]

        for v in var:
            if (env[self.position[0] + v, self.position[1], self.position[2]] != 0 or
                        env[self.position[0],self.position[1] + v,self.position[2]] != 0):
                return True

        return ;

    def findAttachment(self, env , x = 0):
        """
        moves downwards until finds a place to attach itself and attaches itself there
        Args:
            env: 3D int array showing the discrete environment.
            x: int between 0 and 3 indicating the direction of the edge.
        """
        #perform step to get over edge
        if x == 0:
            self.position[0] += 1
        elif x == 1:
            self.position[0] -= 1
        elif x ==2:
            self.position[1] += 1
        else:
            self.position[1] -= 1

        #move downward
        self.position[2] -= 1
        hasFriend = self.findFriends(env)
        while (env[self.position[0], self.position[1], self.position[2] - 1] == 0
                and hasFriend):
            self.position[2] -= 1
            if (self.findFriends(env) == False):
                hasFriend = False

        if hasFriend == False:
            self.position[2] += 1
            self.attached = True
        #env[self.position[0], self.position[1], self.position[2] - 1] == 0:
        self.attached = True

        return;

    def moveAnt(self, randNum, env):
        """
        moves ant in the direction the randNum indicates, 0:x+1, 1:x-1, 2:y+1, 3: y-1, if position is free
        if doesn't have an ant below -> edgeDetected=True and stay where it was.
        Args:
            randNum: int between 0 and 3 indicating the direction that the ant walks.
            env: 3D int array showing the discrete environment.
        Returns:
            Bool: True if an actual movement was performed, False otherwise.
        """

        #print('movingAnt ', randNum)
        moved = False
        if randNum == 0:
            if (self.checkboundaries(env, [self.position[0] + 1, self.position[1], self.position[2]])
                and self.checkOccupied(env, [self.position[0] + 1, self.position[1], self.position[2]])):
                if self.checkEdgeDetected(env, [self.position[0] + 1, self.position[1], self.position[2] - 1] ):
                    self.edgeDetected=True
                    return moved;
                else:
                    self.position[0] += 1
                    moved = True

        elif randNum == 1:
            if (self.checkboundaries(env, [self.position[0] - 1, self.position[1], self.position[2]])
            and self.checkOccupied(env, [self.position[0] - 1, self.position[1], self.position[2]])):
                if self.checkEdgeDetected(env, [self.position[0] - 1, self.position[1], self.position[2] - 1]):
                    self.edgeDetected=True
                    return moved;
                else:
                    self.position[0] -= 1
                    moved = True

        elif randNum == 2:
            if (self.checkboundaries(env, [self.position[0], self.position[1] +1, self.position[2]])
                and self.checkOccupied(env, [self.position[0], self.position[1] + 1, self.position[2]])):
                    if self.checkEdgeDetected(env, [self.position[0], self.position[1] +1, self.position[2] - 1]):
                        self.edgeDetected=True
                        return moved;
                    else:
                        self.position[1] += 1
                        moved = True

        else:
            if (self.checkboundaries(env, [self.position[0], self.position[1] - 1, self.position[2]])
                and self.checkOccupied(env, [self.position[0], self.position[1] - 1, self.position[2]])):
                    if self.checkEdgeDetected(env, [self.position[0], self.position[1] - 1, self.position[2] - 1]):
                        self.edgeDetected=True
                        return moved;
                    else:
                        self.position[1] -= 1
                        moved = True
        return moved;


    def checkAttach(self, env, probability):
        """
        One step of an attached ant. It checks if it should let go and start a random walk.
         Args:
            env: 3D int array showing the discrete environment.
            probability: double between 0 and 1, the probability an ant lets go if it can.
        """
        index = [0, 1]
        var = [-1, 1]
        friends = 0
        counter = 0
        movement = False
        if (self.attached):
            if (self.checkboundaries(env, [self.position[0], self.position[1], self.position[2] + 1]) and
                        env[self.position[0], self.position[1], self.position[2] + 1] == 0):
                for v in var:
                    if (env[self.position[0] + v, self.position[1], self.position[2]] != 0):
                        friends += 1
                    if (env[self.position[0], self.position[1] + v, self.position[2]] != 0):
                        friends += 1

                if friends < 3 and random.uniform(0, 1) < probability:
                    # start randomwalk by doing a first step up and then to one side
                    #print('Ant released at ', self.position)
                    self.attached = False
                    if friends > 1:
                        self.position[2] += 1
                        #print('Ant moved up to ', self.position)

                    while movement==False and counter < 4:
                        counter += 1
                        x = randint(0, 3)
                        movement = self.moveAnt(x, env)
                        #print('Ant made step to ', self.position)
                    if counter >=4:
                        self.position[2] -= 1
                        self.attached = True
                    #print('Ant stopped at ', self.position)
        return;


    def randomwalk(self, env, attachprob):
        """
        One step of a non-attached ant. It walks randomly and connects to the raft if it reaches an edge with a
        certain probability.
        Args:
                env: 3D int array showing the discrete environment.
                attachprob: double between 0-1 probability that a random walk ant attaches to an edge
        """
        x = randint(0, 3)
        self.moveAnt(x, env)
        if (self.edgeDetected and random.uniform(0, 1) < attachprob):
            self.findAttachment(env, x)
        else:
            self.edgeDetected = False
        return;


    def checkboundaries(self, env, position=[0, 0, 0]):
        """
        Probing if a position is out of bound.
            Args:
                env: 3D int array showing the discrete environment.
                position: int array with 3 entries for x, y and z
            Returns:
                Bool: True if it is in bounds and False if position is out of bounds.
        """
        if all(np.asarray(position) < env.shape):
            return True;
        else:
            return False;
        return;


    def performstep(self, env, releaseprob, attachprob):
        """
        Performing a step of the ant - either staying attached or performing a random walk step.
            Args:
                env: 3D int array showing the discrete environment.
                releaseprob: double between 0-1 probablility that an attached ant at the edge lets go and starts walking
                attachprob: double between 0-1 probability that a random walk ant attaches to an edge
            Returns:
                position: Int array with 3 elements indicating the current/new position of the ant.
        """
        if self.attached:
            self.checkAttach(env, releaseprob)
        else:
            self.randomwalk(env, attachprob)
        return self.position;

    def checkOccupied(self, env, position=[0,0,0]):
        """
        Checking if the indicated position is still free.
            Args:
                env: 3D int array showing the discrete environment.
                position: Int array with 3 elements indicating the current/new position of the ant.
            Returns:
                Bool: True if the cube is free, otherwise false

        """
        if env[tuple(position)]!=0:
            return False;
        return True;

    def checkEdgeDetected(self, env, position = [0,0,0]):
        """
        Checking if the indicated position is still free.
            Args:
                env: 3D int array showing the discrete environment.
                position: Int array with 3 elements indicating the current/new position of the ant.
            Returns:
                Bool: True if the cube under the ant is free, otherwise false

                """
        if(env[tuple(position)]==0):
            return True;
        return False;