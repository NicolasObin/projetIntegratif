#!/usr/bin/env python

import sys
import time
import subprocess
import os

"""
from posturev3 import *
import tfct
"""

from importFiles import command_scp 

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule


def Init(robotIP, PORT):
	try:
		broker = ALBroker("pythonBroker", "0.0.0.0", 9559, robotIP, PORT)
	except Exception,e:
		print "Could not create proxy to ALBroker"
		print "Error was: ",e
		sys.exit(1)
	
	try:
		recorder = ALProxy("ALAudioRecorder", robotIP, PORT)
	except Exception,e:
		print "Could not create proxy to ALAudioRecorder"
		print "Error was: ",e
		sys.exit(1)
	try:
		parole = ALProxy("ALTextToSpeech", robotIP, PORT)
	except Exception,e:
		print "Could not create proxy to ALTextToSpeech"
		print "Error was: ",e
		sys.exit(1)
	
	try:
		impro = ALProxy("ALAudioPlayer", robotIP, PORT)	
	except Exception,e:
		print "Could not create proxy to ALAudioPlayer"
		print "Error was: ",e
		sys.exit(1)
	
	return [broker,recorder,parole,impro]

class myModule(ALModule):
	def soundChanged(self, strVarName, value, strMessage):
		global events
		if value[1][0] > 0:
			events = True

if __name__ == "__main__":
	
	from optparse import OptionParser
	"""
	Usage: NAO_Activate_Recording.py [opts]
	Example:
		./NAO_Activate_Recording.py -d 30 -f /home/nao/recordings/test5.wav -o /home/emilie/Bureau/NAO/
	"""

	
	parser = OptionParser()
	parser.add_option("-f","--file",dest = "filename", help = "Path to the output audio file in .wav")
	parser.add_option("-d","--duration",dest = "duration", help = "Duration of your recording")
	parser.add_option("-o","--odir",dest = "odir", help = "Path to the output directory in your computer")

	parser.set_defaults(filename = '/home/nao/recordings/audio_acquisition.wav',duration = 5)

	(option,args) = parser.parse_args()

	filename = option.filename
	duration = option.duration
	ordidir = option.odir

	# Initialisation
	robotIP='nao.local'
	PORT = 9559
	[broker,recorder,parole,impro] = Init(robotIP,PORT)
	

	events = False
	pythonModule = myModule("pythonModule")
	
	localisation = ALProxy("ALAudioSourceLocalization", robotIP, PORT)
	accessmemory = ALProxy("ALMemory", robotIP, PORT)
	# En attente d'une interaction sonore
	while False == events:
		accessmemory.subscribeToEvent("ALAudioSourceLocalization/SoundLocated", "pythonModule", "soundChanged")
		localisation.subscribe("MyApplication")

	# Enregistrement
	#from mvmt_propre import NaoMouvement
	#NaoMouvement(1,15,robotIP,PORT,True)
	recorder.stopMicrophonesRecording()
	parole.say("I'm listening to you")
	localisation.unsubscribe("MyApplication")
	accessmemory.unsubscribeToEvent("ALAudioSourceLocalization/SoundLocated", "pythonModule", "soundChanged")
	recorder.startMicrophonesRecording(filename,"wav",16000,[1,1,1,1])
	time.sleep(float(duration))
	recorder.stopMicrophonesRecording()
	
	# Exportation
	chemin = "C:\Users\ismail\Desktop\Robot_Musicien\Robot_Musicien\Code_NAO\audio_rec"
	[outname,ordiname] = command_scp(filename,chemin,False,robotIP) # Nao -> Ordi
	#time.sleep(5)

	# Filtrage
	#tfct.filtrage(ordiname, ordiname)

	# PyOracle
	print "PyOracle"
	from functionsLibrary import runBeatTracking, runPyOracle
	[out_impro,seq_len] = runPyOracle(ordiname)
	print out_impro

	# Beat-tracker
	print "Beat-Tracker"
	[out_beat,first] = runBeatTracking(ordiname) # base sur l'audio
	print out_beat 
	#out_beat = runBeatTracking(ordiname)

	# Exportation 
	[outname2,ordiname] = command_scp(out_impro,ordidir,True,robotIP) # Ordi -> Nao
	#time.sleep(1)
	try:
        	while True:
			# Sortie audio
			impro.post.playFile(outname2)
			# Commande de mouvement
			#NaoMouvement(out_beat/2,float(duration)/2,robotIP,PORT,False)
			#impro.stopAll()
			#motion.setStiffnesses("Body", 0.0)
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		impro.stopAll()
		broker.shutdown()
		sys.exit(0)
	
	

	
	
					

				




	
