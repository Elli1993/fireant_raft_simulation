# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:18:33 2018

"""

#from ant import ant
from enviroment import environment
import numpy as np
import csv

bound = 150
zbound = 30
steps = 5000
env = environment([bound, bound, zbound])
statistics = np.zeros([zbound, steps])

#messen von zeit /steps bis sich ein layer gany auflöst - parameter ändern und das beobachten

env.setAnts(500, 'cube')
#env.showAnts(save=True, index = [0,0], show=False)
#env.moveOneAnt(49)

for i in range(steps):
    print('Current index ', i)
    #for index in range(300):
        #bool = env.moveOneAnt(index)
        #if bool:
            #env.showAnts(save=True, index= [i,index], show=False)

        #if env.env[env.ants[index].position[0], env.ants[index].position[1], env.ants[index].position[2] +1] != 0:
            #if not env.ants[index].attached:
                #print('WARNINGNNNGNGNG something is wrong')
    env.performStep(releaseprob=0.5, attachprob=0.5)
    for layer in range(zbound):
        if not np.all(env.env[:,:,layer]==0):
            statistics[layer, i] = 1
        if statistics[layer, i] != statistics[layer, i-1]:
            print('current index: ' , i)
            print('change in layer', layer, 'from ', statistics[layer, i-1], 'to', statistics[layer, i])
    #check if there's an ant moving even though there is someone on top
    #env.showAnts(save=True, index=[0, i], show=False)

x =statistics[~(statistics==0).all(1)]
print(x)
np.savetxt('test.csv', x, delimiter=',', fmt='%d')
print('datasaved')
env.showAnts(save=True, index =[0,0], show=True)

numberOfAnts = np.count_nonzero(env.env)
print('Number of ants at end ', numberOfAnts)
#env.createGif('movie.gif')
#env.saveAnts()
#env.loadAnts()



