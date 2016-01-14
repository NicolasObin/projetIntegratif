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
		
	return [recorder,parole]

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
	[recorder,parole] = Init(robotIP,PORT)
	
	# Enregistrement
	parole.say("vous pouvez parlez")
	recorder.startMicrophonesRecording(filename,"wav",48000,[1,1,1,1])
	time.sleep(float(duration))
	recorder.stopMicrophonesRecording()
	parole.say("merci")
	
	# Exportation Nao -> Ordi
	chemin = "/home/ismail/Documents/nao/NAO_I4/audio_rec/"
	[outname,ordiname] = command_scp(filename,chemin,False,robotIP) 

	
	
					

				




	
