#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

'''exemple : tourner la tête du nao'''
import sys
import math
import motion
import time
from naoqi import ALModule, ALBroker, ALProxy

robotIP='nao.local'
PORT = 9559

try:
    motion = ALProxy("ALMotion", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    sys.exit(1)
#setAngles(Nom ,Angle, Vit)
#Nom: partie a bouger
#Angle: tableau 2 dim [X, Y]
#vit: entre 0 et 1
motion.setAngles("Head", [5, -1], 0.3)


