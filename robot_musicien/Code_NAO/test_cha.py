#!/usr/bin/env python

import sys
import math
import os
import time
import numpy
from naoqi import ALProxy, ALBroker, ALModule


robotIP="10.42.0.48"
PORT = 9559

try:
    recorder = ALProxy("ALAudioDevice", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALAudioDevice"
    print "Error was: ",e
    sys.exit(1)	


if __name__ == "__main__":
	recorder.startMicrophonesRecording("/home/nao/recordings/cle_esclangon2.wav") # ,"wav",16000,[0,0,1,0])

	time.sleep(10)

	recorder.stopMicrophonesRecording()
