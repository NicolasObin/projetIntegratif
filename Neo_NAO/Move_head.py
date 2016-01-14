import sys
import math
import motion
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

robotIP= 'nao.local'
PORT = 9559


try:
    broker = ALBroker("pythonBroker", "0.0.0.0", 9559, robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    sys.exit(1)

try:
    motion = ALProxy("ALMotion", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    sys.exit(1)

try:
    sound = ALProxy("ALAudioSourceLocalization", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALAudioSourceLocalization"
    print "Error was: ",e
    sys.exit(1)

try:
    memory = ALProxy("ALMemory",robotIP, PORT)
except Exception,e:
    print "ALMemory error"
    print "Error was: ",e
    sys.exit(1)

try:
    speak = ALProxy("ALTextToSpeech", robotIP, PORT)
except Exception,e:
    print "ALTextToSpeech error"
    print "Error was: ",e
    sys.exit(1)

try:
    recorder = ALProxy("ALAudioDevice", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALAudioDevice"
    print "Error was: ",e
    sys.exit(1)	

try:
    recognition = ALProxy("ALSpeechRecognition", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALAudioDevice"
    print "Error was: ",e
    sys.exit(1)	

#sound.subscribe("Sensibility") 
#sound.subscribe("EnergyComputation")

#sound.setParameter("Sensibility",0.4)
#sound.setParameter("EnergyComputation",True)

#a=memory.getData("Music")
#source = memoryproxy.getData("ALAudioSourceLocalization/SoundLocated")
motion.setStiffnesses("Head",1.0)

class myModule(ALModule):
   """callback module"""
   def soundChanged(self, strVarName, value, strMessage):
     """callback function"""
     motion.setAngles(["HeadPitch", "HeadYaw"], [0, value[1][0]], 0.3)
     #if value[1][0] < 0:
     #   print "Turn right", -value[1][0], "radians"
     #else:
     #   print "Turn left", value[1][0], "radians"


pythonModule = myModule("pythonModule")

memory.subscribeToEvent("ALAudioSourceLocalization/SoundLocated", "pythonModule", "soundChanged")

sound.subscribe("MyApplication")

#time.sleep(30)
#recorder.startMicrophonesRecording("/home/nao/recordings/Test_Antonyo.wav")
time.sleep(30)
#recorder.stopMicrophonesRecording()

sound.unsubscribe("MyApplication")
memory.unsubscribeToEvent("ALAudioSourceLocalization/SoundLocated", "pythonModule", "soundChanged")
motion.setStiffnesses("Head",0.0)
