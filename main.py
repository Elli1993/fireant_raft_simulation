# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:33 2018

"""

from ant import ant
from enviroment import environment


env = environment([10,10,10])

env.setAnts(50, 'cube')
env.showAnts(save=True, index = [0,0], show=False)
#env.moveOneAnt(49)
for i in range(1):
    for index in range(50):
        bool = env.moveOneAnt(index)
        if bool:
            env.showAnts(save=True, index= [i,index], show=False)

env.createGif('move.gif')
#env.saveAnts()
#env.loadAnts()



