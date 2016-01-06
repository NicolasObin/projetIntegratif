#!/usr/bin/env python

import sys
import time
import subprocess
import os
from posturev2 import *
from naoqi import ALProxy,ALModule,ALBroker
from mvmt_propre import NaoMouvement

impro = ALProxy("ALAudioPlayer","10.42.0.48", 9559)

impro.post.playFile('/home/nao/recordings/demo_eval.wav')
time.sleep(0.5)
NaoMouvement(0.6,15,"10.42.0.48", 9559,False)
impro.stopAll()
