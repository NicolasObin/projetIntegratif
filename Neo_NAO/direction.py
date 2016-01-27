#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

'''Walk: Small example to make Nao walk'''
import sys
import motion
import time
from naoqi import ALProxy
import numpy as np
from subprocess import Popen, PIPE


def Init (robotIP, PORT):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    return [motionProxy, postureProxy]

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

#fonction qui permet de faire tourner le robot 
def Rotation(toto, motionProxy):
    if toto == 1:
        #gauche = 90 
        X = 0.0
        Y = 0.0
        Theta = np.pi/2
    else:
        #droite = -90° 
        X = 0.0
        Y = 0.0
        Theta = -np.pi/2
    #print "rotate /n"
    #motionProxy.post.moveTo(X, Y, Theta)
    return Theta

#fonction qui permet de faire marcher le robot 
def Marcher(motionProxy):
    #marche sur 1m20
    print "marcher"
    X = 1.2
    Y = 0.0
    Theta = 0
    #motionProxy.post.moveTo(X, Y, Theta) 
    return X, Y
      

def paramNao(robotIP, motionProxy, postureProxy):
    
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Walk algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)
    #~ motionProxy.setWalkArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])


def moveTo(robotIP, PORT, toto):
    [motionProxy, postureProxy] = Init(robotIP, PORT)
    theta = Rotation(toto, motionProxy)
    time.sleep(3.5)  
    x, y = Marcher(motionProxy)
    time.sleep(3.5)  

    #motionProxy.moveInit()
    return x, y, theta


