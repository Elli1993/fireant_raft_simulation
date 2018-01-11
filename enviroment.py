# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:31 2018

"""

import numpy as np
import os
import math
import ant
#import random !!!

class environment(object):
    '''
    Class simulating the environment for the ant raft.
    self.env is a in 3D-array, coding each discrete position in the environment. It contains 0 for free cubes,
    1 for ants that are moving around and 2 for attached ants.
    self.numUpdates keeps track of the iterations performed on the environment.
    self.numAnts shows the number of active ants.
    '''


    def __init__(self, dimensions = [100, 100, 100]):
        """
        Args:
            dimensions: int array with entries specifying the x, y and z dimensions of the env
        """
        self.env = np.zeros(dimensions)
        self.dimensions = np.asarray(dimensions)
        self.numUpdates = 0
        self.numAnts = 0
        self.ants = []

        return;
    
    def setAnts(self, number = 200, config = 'cube'):
        """
        Args: 
            number: int, number of ants
            config: string, specifying the initial configuration of ants: random, circle, cube....
        """
        self.numAnts = number

        if number >= (self.dimensions[0]*self.dimensions[1]*self.dimensions[2])/0.7:
            print('Too many ants for this configuration!')

        if (config == 'random'):
            print('Setting ants up randomly in the environment.')
            print('The function setAnts - random is not yet implemented.')

        if (config == 'ball'):
            print('Setting ants up in a tight ball.')
            print('The function setAnts - ball is not yet implemented.')
            middlepoint = self.dimensions / 2

        if (config == 'cube'):
            print('Setting ants up in a cube.')
            middlepoint = self.dimensions / 2
            sidelength = np.floor(number**(1./3.))
            startpoint = np.ndarray.astype(middlepoint - sidelength/2 , int)
            countx = county = 0
            #print('Sidelength is: ',sidelength)

            for ant in range(number):
                self.ants.append(ant.__init__(startpoint, ant))
                self.env[tuple(startpoint)] = 2
                #print('Ant set at ', startpoint)
                if countx < sidelength:
                    # increase position in x direction
                    startpoint[0] += 1
                    countx += 1
                elif county < sidelength:
                    # increase position in y direction and reset x
                    startpoint[0] -= sidelength
                    startpoint[1] += 1
                    countx = 0
                    county += 1
                else:
                    # increase z position and reset x & y - build a notfull layer if not a cubic num of ants
                    startpoint[0] -= sidelength
                    startpoint[1] -= sidelength
                    startpoint[2] += 1
                    countx = 0
                    county = 0
            print('Ants all set.')

        else:
            print('Invalid initial configuration of the ant environment!')

        return;

    def showAnts(self):
        for i in range(self.dimensions[2]):
            print(np.matrix(self.env[:,:,i]))

    def loadAnts(self, file):
        """
        Args: 
            file: file handle to load ants from a file
        """

        return;

    def saveAnts(self, file):
        """
        Args: 
            file: file handle to save ants in a file
        """

        return; 