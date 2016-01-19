#code pour ipython
'''
from naoqi import ALProxy
import motion

m = ALProxy("ALMotion", 'nao.local', 9559)

p = ALProxy("ALRobotPosture", 'nao.local', 9559)


p.goToPosture("Stand", 0.5)

m.setAngles(["LShoulderPitch", "RShoulderPitch"], [0, 0], 0.2)


m.getJointNames("Arms")'''


import sys
from naoqi import ALProxy
import time
import numpy as np

def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e


    motionProxy.setStiffnesses("Head", 1.0)
    postureProxy.goToPosture("StandInit", 0.4)
    
    # Example showing how to set angles, using a fraction of max speed
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [0, -1]
    fractionMaxSpeed  = 0.3
    # bouger la tete
    #motionProxy.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(1)
    names  = ["LShoulderPitch"]
    angles  = [-np.pi/3]
    fractionMaxSpeed= 0.3
    #bouger le bras gauche
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(2)

    x = 0.2
    y = 0
    theta_goal = 0
    motionProxy.moveInit()
    motionProxy.post.moveTo(x, y, theta_goal)
    


if __name__ == "__main__":
    robotIp = 'nao.local'

    if len(sys.argv) <= 1:
        print "Usage python almotion_setangles.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
