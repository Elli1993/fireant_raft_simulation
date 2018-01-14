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

    def randomwalk(self, env,count,probAttach,maxSteps):
        """
        One step of a non-attached ant. It walks randomly and connects to the raft if it reaches an edge with a
        certain probability.
            """

        if (self.edgeDetected and random.uniform(0,1)< probAttach):
            self.findAttachment(env)
        elif (self.edgeDetected == False and count < maxSteps ):
            count+=1
            x = randint(0, 3)
            self.moveAnt(x, env)
            self.randomwalk(env,count,probAttach,maxSteps)
        else:
            self.attached=True
        return;

    def checkAttach(self, env, probAttach=0.5, maxSteps=50):
        """
        One step of an attached ant. It checks if it should let go and start a random walk.
        """
        index = [0, 1]
        var = [-1, 1]
        friends = 0
        movement=False
        counter =0
        flag = False
        print( 'starting pos ', self.position)
        if (self.attached):
            if (env[self.position[0], self.position[1], self.position[2] + 1] == 0):
                for v in var:
                    if (env[self.position[0] + v, self.position[1], self.position[2]] != 0):
                        friends += 1
                    if (env[self.position[0], self.position[1] + v, self.position[2]] != 0):
                        friends += 1
                #print("friends:", friends)
                if friends < 3 and random.uniform(0, 1) < probAttach:
                    # start randomwalk by doing a first step up and then to one side
                    print('walking starts')
                    if friends > 1:
                        self.position[2] +=1
                        flag=True

                    while movement == False and counter < 4:
                        counter += 1
                        x = randint(0, 3)
                        movement = self.moveAnt(x, env)
                        #print('Ant made step to ', self.position)
                    #print(self.position)
                    #print(movement)
                    if counter >=4 and movement == False:
                        if flag:
                            #print('inflag')
                            self.position[2] -= 1
                        self.attached = True


                    if self.edgeDetected and self.attached ==False and random.uniform(0,1) < probAttach:
                        self.findAttachment(env)
                    else:
                        self.edgeDetected = False
                    # movement only true if no edge detected
                    if movement == True:
                        self.randomwalk(env, 0, maxSteps, probAttach)

        print('end pos ', self.position)
        return;

    def getPosition(self):
        x = self.position
        return x;

    def findAttachment(self, env , x = 0):
        """
        moves downwards until finds a place to attach itself and attaches itself there
        Args:
            env: 3D int array showing the discrete environment.
            x: int between 0 and 3 indicating the direction of the edge.
        """
        #perform step to get over edge
        #TODO sometimes it still gets here even though the position is taken
        #TODO ant continues to go down even if it does no longer have friends
        if x == 0:
            if self.checkOccupied(env, [self.position[0] + 1, self.position[1], self.position[2]]):
                self.position[0] += 1
            else:
                self.attached = True
                return;
        elif x == 1:
            if self.checkOccupied(env, [self.position[0] - 1, self.position[1], self.position[2]]):
                self.position[0] -= 1
            else:
                self.attached = True
                return;
        elif x ==2:
            if self.checkOccupied(env, [self.position[0], self.position[1] +1 , self.position[2]]):
                self.position[1] += 1
            else:
                self.attached = True
                return;
        else:
            if self.checkOccupied(env, [self.position[0], self.position[1] - 1 , self.position[2]]):
                self.position[1] -= 1
            else:
                self.attached = True
                return;
        #move downward
        if self.checkboundaries(env, [self.position[0], self.position[1], self.position[2]-1]):
            if self.checkOccupied(env, [self.position[0], self.position[1], self.position[2]-1]):
                self.position[2] -= 1
            else:
                self.attached = True
                return;
        hasFriend = self.findFriends(env)
        while (env[self.position[0], self.position[1], self.position[2] - 1] == 0
                and hasFriend):
            if self.checkboundaries(env, [self.position[0], self.position[1], self.position[2] - 1]):
                self.position[2] -= 1
            else:
                print('somehow at the bottom!!!!!')
                self.attached = True
                return ;
            if (self.findFriends(env) == False):
                hasFriend = False

        if hasFriend == False:
            if self.checkOccupied(env,[self.position[0], self.position[1], self.position[2] +1]):
                self.position[2] += 1
                self.attached = True
        #env[self.position[0], self.position[1], self.position[2] - 1] == 0:
        self.attached = True


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
        """
        Checking if the indicated position is still free.
            Args:
                env: 3D int array showing the discrete environment.
                position: Int array with 3 elements indicating the current/new position of the ant.
            Returns:
                Bool: True if the cube is free, otherwise false

        """
        if env[tuple(position)] != 0:
            return False;
        return True;

    def checkEdgeDetected(self, env, position=[0, 0, 0]):
        """
        Checking if the indicated position is still free.
            Args:
                env: 3D int array showing the discrete environment.
                position: Int array with 3 elements indicating the current/new position of the ant.
            Returns:
                Bool: True if the cube under the ant is free, otherwise false

                """
        if (env[tuple(position)] == 0):
            return True;
        return False;

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
            if (self.checkboundaries(env, [self.position[0] + 1, self.position[1], self.position[2]])):
                if self.checkOccupied(env, [self.position[0] + 1, self.position[1], self.position[2]]):
                    if self.checkEdgeDetected(env, [self.position[0] + 1, self.position[1], self.position[2] - 1] ):
                        self.edgeDetected=True
                        return moved;
                    else:
                        self.position[0] += 1
                        moved = True

        elif randNum == 1:
            if (self.checkboundaries(env, [self.position[0] - 1, self.position[1], self.position[2]])):
                if self.checkOccupied(env, [self.position[0] - 1, self.position[1], self.position[2]]):
                    if self.checkEdgeDetected(env, [self.position[0] - 1, self.position[1], self.position[2] - 1]):
                        self.edgeDetected=True
                        return moved;
                    else:
                        self.position[0] -= 1
                        moved = True

        elif randNum == 2:
            if (self.checkboundaries(env, [self.position[0], self.position[1] +1, self.position[2]])):
                if self.checkOccupied(env, [self.position[0], self.position[1] + 1, self.position[2]]):
                        if self.checkEdgeDetected(env, [self.position[0], self.position[1] +1, self.position[2] - 1]):
                            self.edgeDetected=True
                            return moved;
                        else:
                            self.position[1] += 1
                            moved = True

        else:
            if (self.checkboundaries(env, [self.position[0], self.position[1] - 1, self.position[2]])):
                if self.checkOccupied(env, [self.position[0], self.position[1] - 1, self.position[2]]):
                    if self.checkEdgeDetected(env, [self.position[0], self.position[1] - 1, self.position[2] - 1]):
                        self.edgeDetected=True
                        return moved;
                    else:
                        self.position[1] -= 1
                        moved = True
        return moved;





