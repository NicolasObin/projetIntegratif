#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

'''exemple : déplacer le nao avec une position précise'''
import sys
import math

import time
from naoqi import ALModule, ALBroker, ALProxy

robotIP='nao.local'

PORT = 9559

def main(robotIP):
    """ robot Position: Small example to know how to deal
                        with robotPosition and getFootSteps
    """

    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in stiffness On
    StiffnessOn(motionProxy)
    postureProxy.goToPosture("StandInit", 0.5)

motionProxy = ALProxy("ALMotion", robotIP, 9559)
# created a walk task
motionProxy.moveInit()
motionProxy.moveTo(0.5, 0.0, 0.0)


# wait that the move process start running
time.sleep(0.1)

# get robotPosition and nextRobotPosition
robotPosition     = motionProxy.getRobotPosition(True)
nextRobotPosition = motionProxy.getNextRobotPosition(True)
print robotPosition
print nextRobotPosition
#diff = [nextRobotPosition]-[robotPosition]
#print "la distance est de "+diff

motionProxy.post.moveTo(0.0, 0.0, 0.0)
