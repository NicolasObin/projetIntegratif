import sys
import math
import motion
import time
from naoqi import ALModule, ALBroker, ALProxy

robotIP="192.168.2.4"
PORT = 9559


broker = ALBroker("pythonBroker", "0.0.0.0", 9999, robotIP, PORT)
motion = ALProxy("ALMotion", robotIP, PORT)
sound = ALProxy("ALAudioSourceLocalization", robotIP, PORT)
memory = ALProxy("ALMemory",robotIP, PORT)
speak = ALProxy("ALTextToSpeech", robotIP, PORT)
recorder = ALProxy("ALAudioDevice", robotIP, PORT)
recognition = ALProxy("ALSpeechRecognition", robotIP, PORT)

class myModule2(ALModule):
  """callback module"""
  def wordChanged(self, strVarName, value, strMessage):
    """callback function"""
    print (value[1]) 
    if value[1] > 0.6:
       print "Word recognized is", value[0]

pythonModule = myModule2("pythonModule")


recognition.setVocabulary(["Nao", "Danse","Listen"], True)

memory.subscribeToEvent("WordRecognized", "pythonModule", "wordChanged")

recognition.subscribe("MyApplication2")
time.sleep(15)
recognition.unsubscribe("MyApplication2")

memory.unsubscribeToEvent("WordRecognized", "pythonModule", "wordChanged")

