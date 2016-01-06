#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import sys
import time
from naoqi import ALProxy,ALModule,ALBroker

robotIP="10.42.0.48"
PORT = 9559


try:
	broker = ALBroker("pythonBroker", "0.0.0.0", 9999, robotIP, PORT)
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
    recorder = ALProxy("ALAudioDevice", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALAudioDevice"
    print "Error was: ",e
    sys.exit(1)	

try:
    parole = ALProxy("ALTextToSpeech", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ",e
    sys.exit(1)	

try:
    recognition = ALProxy("ALSpeechRecognition", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALSpeechRecognition"
    print "Error was: ",e
    sys.exit(1)	

class myModule(ALModule):
	def WordDectected(self, strVarName, value, strMessage):
		global events
		events = True



if __name__ == "__main__":

	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-f","--file",dest = "filename", help = "Path to the output audio file in .wav")

	parser.set_defaults(filename = '/home/nao/recordings/audio_acquisition.wav')

	(option,args) = parser.parse_args()

	filename = option.filename
	
	events = False
	pythonModule = myModule("pythonModule")
	
	accessmemory = ALProxy("ALMemory", robotIP, PORT)

	recognition.setVocabulary(["Nao","toto"],True)

	while False == events:
	
		accessmemory.subscribeToEvent("WordRecognized", "pythonModule", "WordDectected")
		recognition.subscribe("MyApplication")
		parole.say("J'attends tes ordres maitre")
		time.sleep(5)

	recognition.unsubscribe("MyApplication")
	accessmemory.unsubscribeToEvent("WordRecognized", "pythonModule", "WordDectected")
	parole.say("Vas y! Je t'écoute")
#	recorder.startMicrophonesRecording(filename)

	#time.sleep(5)

	#recorder.stopMicrophonesRecording()
	parole.say("Ok done")
	broker.shutdown()
	

	
	
					

				




	
