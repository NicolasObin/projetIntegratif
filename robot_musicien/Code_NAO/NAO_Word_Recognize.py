import sys
import math
import motion
import time
from naoqi import ALModule, ALBroker, ALProxy

robotIP="10.42.0.48"
PORT = 9559

broker = ALBroker("pythonBroker", "0.0.0.0", 9999, robotIP, PORT)
memory = ALProxy("ALMemory",robotIP, PORT)
recognition = ALProxy("ALSpeechRecognition", robotIP, PORT)

class myModule(ALModule):
  """callback module"""
  def wordChanged(self, strVarName, value, strMessage):
    """callback function"""
    print (value[1]) 
    if value[1] > 0.6:
       print "Word recognized is", value[0]

pythonModule = myModule("pythonModule")

recognition.setVocabulary(["Nao", "Danse","Listen"], True)
memory.subscribeToEvent("WordRecognized", "pythonModule", "wordChanged")

recognition.subscribe("MyApplication2")
time.sleep(15)
recognition.unsubscribe("MyApplication2")

memory.unsubscribeToEvent("WordRecognized", "pythonModule", "wordChanged")

