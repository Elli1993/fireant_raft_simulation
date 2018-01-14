# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:33 2018

"""

from ant import ant
from enviroment import environment
import numpy as np

bound = 20
zbound = 20
env = environment([bound,bound,zbound])

env.setAnts(50, 'cube')
env.showAnts(save=True, index = [0,0], show=False)
#env.moveOneAnt(49)
for i in range(20):
    for index in range(50):
        bool = env.moveOneAnt(index)
        if bool:
            env.showAnts(save=True, index= [i,index], show=False)

numberOfAnts = np.count_nonzero(env.env)
print('Number of ants at end ', numberOfAnts)
env.createGif('movie.gif')
#env.saveAnts()
#env.loadAnts()



