# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:31 2018

"""

import numpy as np
import os
#import random !!!

class environment(object):
    '''
    Class simulating the environment for the ant raft.
    self.env is a in 3D-array, coding each discrete position in the environment. It contains 0 for free cubes,
    1 for ants that are moving around and 2 for attached ants.
    self.numUpdates keeps track of the iterations performed on the environment.
    '''


    def __init__(self, dimensions = [100, 100, 100]):
        """
        Args:
            dimensions: int array with entries specifying the x, y and z dimensions of the env
        """
        self.env = np.zeros(dimensions)
        self.numUpdates = 0

        return;
    
    def setAnts(self, number, config):
        """
        Args: 
            number: int, number of ants
            config: string, specifying the initial configuration of ants: random, circle, cube....
        """

        return;

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