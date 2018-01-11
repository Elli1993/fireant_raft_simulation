# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:17:52 2018

"""

import numpy as np
import os


class ant(object):
    '''
    Object simulating a single ant that can interact with the environment.
    Ants have self.position giving their current position in the environment and self.attached indicating if they
    are currently attached to the raft.
    '''

    def __init__(self, position = [0, 0, 0]):
        """
        Initialize the ant and position it in the environment.
        Args:
            position: int array giving the initial position of the ant.
            """
        self.position = position
        self.attached = False

        return;

    def randomwalk(self):
        """
        One step of a non-attached ant. It walks randomly and connects to the raft if it reaches an edge with a
        certain probability.
            """
        return;

    def checkAttach(self):
        """
        One step of an attached ant. It checks if it should let go and start a random walk.
        """
        return;
