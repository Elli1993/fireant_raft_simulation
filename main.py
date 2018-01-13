# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:33 2018

"""

from ant import ant
from enviroment import environment


env = environment([10,10,10])

env.setAnts(50, 'cube')
env.showAnts()
env.moveOneAnt(49)
#for i in range(10):
#    env.performStep()
env.showAnts()
#env.saveAnts()
#env.loadAnts()



