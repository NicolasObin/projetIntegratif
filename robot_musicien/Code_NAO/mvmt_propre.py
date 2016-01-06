#!/usr/bin/env python

import os
import time
from random import randrange
from posturev3 import *
from naoqi import ALProxy

def NaoMouvement(beatMoyen,lenSon,IP,PORT,posInit):
	mvm = ALProxy("ALMotion",IP,PORT)
	lum = ALProxy("ALLeds",IP,PORT)
	rec = ALProxy("ALAudioDevice",IP,PORT)

	#Choix de la danse:
	if posInit == True:
		case = 0
	else:
		case = randrange(1,6,1) #0 = position d ecoute; 1,..,6 = danse
	roboDance = Dance(case)

	#Preparer le robot a danser:
	mvm.setStiffnesses("Body", 1.0)

	#Effectuer le mouvement choisi parmi le fichier posture &  	enregistrement de son en meme temps:
	lengthAudio = lenSon #duree de l impro du robot
	if beatMoyen < 0.5:
		beatSpeed = 2*beatMoyen
	else: 
		beatSpeed = beatMoyen
	nbRepeat = int((lengthAudio/beatSpeed)/roboDance.nbTemps)

	#rec.post.startMicrophonesRecording("/tmp/enregistrement.wav") 	#debut de l enregistrement du son autour de Nao

	name = 'AllLeds'
	intensity = 0
	duration = 0.08
	lum.off(name)

	for m in range(1,nbRepeat):
		print m
		names      = [roboDance.pos1[k][0] for k in range(0,10)]
		angleLists = [roboDance.pos1[k][1] for k in range(0,10)]
		times      = [[beatSpeed] for k in range(0,10)]
		isAbsolute = True
		mvm.angleInterpolation(names, angleLists, times, isAbsolute)
		lum.on(name)
		lum.fade(name, intensity, duration)

		#On suppose que les danses font: min 1temps (ecoute), max 3temps:
		try:
			names      = [roboDance.pos2[k][0]for k in range(0,10)]
			angleLists = [roboDance.pos2[k][1] for k in range(0,10)]
			times      = [[beatSpeed] for k in range(0,10)]
			isAbsolute = True
			mvm.angleInterpolation(names, angleLists, times, isAbsolute)
			lum.on(name)
			lum.fade(name, intensity, duration)
		except:
			pass
	
		try:
			names      = [roboDance.pos3[k][0] for k in range(0,10)]
			angleLists = [roboDance.pos3[k][1] for k in range(0,10)]
			times      = [[beatSpeed] for k in range(0,10)]
			isAbsolute = True
			mvm.angleInterpolation(names, angleLists, times, isAbsolute)
			lum.on(name)
			lum.fade(name, intensity, duration)
	
		except:
			pass
		if case == 0:
			break

	#rec.stopMicrophonesRecording() #fin de l'enregistrement du son autour de Nao

	lum.on(name)

