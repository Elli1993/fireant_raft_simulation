# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:31 2018

"""

import numpy as np
import os
import math
#from ant import ant
from singlestepant import ant
import csv
# import random !!!
import copy
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import imageio


class environment(object):
    '''
    Class simulating the environment for the ant raft.
    self.env is a in 3D-array, coding each discrete position in the environment. It contains 0 for free cubes,
    1 for ants that are moving around and 2 for attached ants.
    self.numUpdates keeps track of the iterations performed on the environment.
    self.numAnts shows the number of active ants.
    '''

    def __init__(self, dimensions=[100, 100, 100]):
        """
        Args:
            dimensions: int array with entries specifying the x, y and z dimensions of the env
        """
        self.env = np.zeros(dimensions)
        self.dimensions = np.asarray(dimensions)
        self.numUpdates = 0
        self.numAnts = 0
        self.ants = []
        self.pictures = []
        self.antsMoved = []
        self.singlestepant = True

        return;

    def setAnts(self, number=200, config='cube'):
        """
        Setting the ants up in a starting configuration.
        Args:
            number: int, number of ants
            config: string, specifying the initial configuration of ants: random, circle, cube....
        """
        self.numAnts = number

        if number >= (self.dimensions[0] * self.dimensions[1] * self.dimensions[2]) / 0.7:
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
            sidelength = np.floor(number ** (1. / 3.))
            startpoint = np.ndarray.astype(middlepoint - sidelength / 2, int)
            countx = county = 0
            # print('Sidelength is: ',sidelength)

            for antindex in range(number):
                currentant = ant(startpoint, antindex)
                self.ants.append(copy.deepcopy(currentant))
                self.env[tuple(startpoint)] = 2
                # print('Ant set at ', startpoint)
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

    def showAntsBin(self):
        """
            Showing the current ant configuration in the console.
        """
        for i in range(self.dimensions[2]):
            print(np.matrix(self.env[:, :, i]))

        return;

    def showAnts(self, save=True, index=[1, 1], show=False):
        """
            Args:
                save: bool, if the picture should be saved
                index: array, included in the name of the picture to be saved
                show: bool, if the picture should be shown during execution
        """
        if not show:
            plt.ioff()
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        plt.ylim((0, self.env.shape[1]))
        plt.xlim((0, self.env.shape[0]))
        ax.set_zlim(0, self.env.shape[2])
        xdata = np.argwhere(self.env == 2)[:, 0]
        ydata = np.argwhere(self.env == 2)[:, 1]
        zdata = np.argwhere(self.env == 2)[:, 2]
        plt.ylabel('y')
        plt.xlabel('x')
        ax.scatter3D(xdata, ydata, zdata, c='b', s=100);
        xdatajustmoved = self.ants[index[1]].position[0]
        ydatajustmoved = self.ants[index[1]].position[1]
        zdatajustmoved = self.ants[index[1]].position[2]
        ax.scatter3D(xdatajustmoved, ydatajustmoved, zdatajustmoved, c='g', s=100)
        xdataalreadymoved = []
        ydataalreadymoved = []
        zdataalreadymoved = []
        for movedant in self.antsMoved:
            if (self.env[tuple(movedant.position)] != 1):
                xdataalreadymoved.append(movedant.position[0])
                ydataalreadymoved.append(movedant.position[1])
                zdataalreadymoved.append(movedant.position[2])
        ax.scatter3D(xdataalreadymoved, ydataalreadymoved, zdataalreadymoved, c='cyan', s=100)
        xdatamove = np.argwhere(self.env == 1)[:, 0]
        ydatamove = np.argwhere(self.env == 1)[:, 1]
        zdatamove = np.argwhere(self.env == 1)[:, 2]
        ax.scatter3D(xdatamove, ydatamove, zdatamove, c='r', s=100);
        if save:
            plt.savefig('ants' + str(index) + '.png')
            self.pictures.append('ants' + str(index) + '.png')
        plt.close(fig)
        return;

    def performStep(self, releaseprob = 0.5, attachprob = 1):
        #print('Performing a step!')
        oldindex = np.zeros(3)
        for antindex in self.ants:
            # print(antindex)
            oldindex = np.copy(antindex.getPosition())
            self.env[tuple(antindex.getPosition())] = 0

            if self.singlestepant:
                antindex.performstep(self.env, releaseprob, attachprob)
            else:
                antindex.checkAttach(self.env, 1)
            newindex = antindex.getPosition()
            if antindex.attached:
                self.env[tuple(newindex)] = 2
            else:
                self.env[tuple(newindex)] = 1
            if any(newindex != oldindex):
                #print('antmoved!', oldindex, newindex)
                self.antsMoved.append(copy.deepcopy(antindex))
        return;

    def moveOneAnt(self, index=0):
        #print('moving ant number ', index)

        oldindex = np.copy(self.ants[index].getPosition())
        self.env[tuple(self.ants[index].getPosition())] = 0

        if self.singlestepant:
            self.ants[index].performstep(self.env, 1, 1)
        else:
            self.ants[index].checkAttach(self.env, 1)
        newindex = self.ants[index].getPosition()
        #if self.env[tuple(newindex)] != 0:
            #print('WAAAAARNNIIINNNNGGG!!!!!')
            #print(self.env[tuple(newindex)])
            #print(self.ants[index].attached)
        if self.ants[index].attached:
            self.env[tuple(newindex)] = 2
        else:
            self.env[tuple(newindex)] = 1
        if any(newindex != oldindex):
            #print('antmoved!', oldindex, newindex)
            self.antsMoved.append(copy.deepcopy(self.ants[index]))
            # print(self.antsMoved)
            return True;
        return False;

    def loadAnts(self, filename='antconfig.csv'):
        """
        Loading ants from a csv file. Reading size from the commented first line.
        Args:
            filename: file handle to load ants from a file
        """
        print('Loading data from ', filename, '.')
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            text = next(reader)
        x = int(text[0][2:])
        y = int(text[1][1:])
        z = int(text[2][1:-1])

        # Read the array from disk
        new_data = np.loadtxt(filename, delimiter=',')

        # However, going back to 3D is easy if we know the
        # original shape of the array
        self.env = new_data.reshape((x, y, z))
        print('Data loaded sucessfully from ', filename, '.')
        return;

    def saveAnts(self, filename='antconfig.csv'):
        """
        Saving ant configuration to a csv. Env shape is saved in a commented out first line.
        Args:
            filename: file handle to save ants in a file
        """

        print('Saving data to ', filename, '.')
        # Write the array to disk
        with open(filename, 'w') as outfile:
            outfile.write('#{0}\n'.format(self.env.shape))

        with open(filename, 'ab') as outfile:
            # Iterating through a ndimensional array produces slices along
            # the last axis. This is equivalent to data[i,:,:] in this case
            for data_slice in self.env:
                np.savetxt(outfile, data_slice, fmt='%d', delimiter=',')

                # Writing out a break to indicate different slices...
                # outfile.write('# New layer\n')

        print('Data saved sucessfully to ', filename, '.')
        return;

    def createGif(self, moviename='movie.gif'):
        """
        Saving the created pictures as a gif.
        Args:
            moviename: file handle to save the gif
        """
        images = []
        print('Creating GIF')
        for filename in self.pictures:
            images.append(imageio.imread(filename))
        imageio.mimsave(moviename, images)
        print('GIF done')
        return;