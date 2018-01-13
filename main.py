# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:33 2018

"""

from ant import ant
from enviroment import environment


env = environment([10,10,10])

env.setAnts(50, 'cube')
env.showAnts()
env.performStep()
env.showAnts()
env.saveAnts()
env.loadAnts()



