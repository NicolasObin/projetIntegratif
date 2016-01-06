#!/usr/bin/env python

import sys
import time
from naoqi import ALProxy

robotIP="192.168.2.4"
PORT = 9559

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


def NAO_Motion(zone,size,speed,angleInit,angle,angleName):

	print "*** "+zone
	print "--- "+ str(angleName)
	print angle
	
	motion.setStiffnesses('Body',1.0)
	
	print "Initial Position"
	motion.setAngles(angleName,angleInit,speed)
	time.sleep(2)
	print "Mouvement"
	motion.setAngles(angleName,angle,speed)
	time.sleep(2)
	print "Initial Position"
	motion.setAngles(angleName,angleInit,speed)

if __name__ == "__main__":

	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-f","--file",dest = "filename")

	(option,args) = parser.parse_args()

	filename = option.filename
	
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read(filename)
	
	if config.has_section('Zone'):
		Zone = config.items('Zone')
 	if config.has_section('Size'):
		Size = config.items('Size')
	if config.has_section('Vitesse'):
		speed = config.items('Vitesse')

	Arm = ["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand","RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand"]
	Leg = ["LHipRoll","LHipPitch","LKneePitch","LAnklePitch","LAnkleRoll","RHipRoll","RHipPitch","RKneePitch","RAnklePitch","RAnkleRoll","LHipYawPitch","RHipYawPitch"]

	
	for z in Zone:
		cmpHead = 0;
		for s in Size:
			if cmpHead == 0:
				for sp in speed:
					name = []	
					angle = []
					if z[1] == 'Head':
						name.extend(["HeadYaw","HeadPitch"])
						angle = config.items('Head')[1:]
						angleInit = config.items('Head')[0]
					elif z[1] == 'Arm':
						name.extend(Arm)
		                         	angle = config.items('Arm')[1:]
						angleInit = config.items('Arm')[0]
						#print angle
						if s[1] == 'L':
							print 'Left Arm'
							angle = angle[0:10]
						elif s[1] == 'R':
							print 'Right Arm'
							angle = angle[10:20]
						elif s[1] == 'B':
							print 'Both Arms'
							angle = angle[20:30]
					elif z[1] == 'Leg':
						name.extend(Leg)
		                         	angle = config.items('Leg')[1:]
						angleInit = config.items('Leg')[0]
						if s[1] == 'L':
							angle = angle[0:10]
						elif s[1] == 'R':
							angle = angle[10:20]
						elif s[1] == 'B':
							angle = angle[20:30]
					for a in angle:
						filename = "/home/nao/recordings/"+z[1]+'_'+s[1]+'_'+sp[1]+'_'+str(a[0])+'.wav'
						recorder.startMicrophonesRecording(filename)
						NAO_Motion(z[1],s[1],float(sp[1]),map(float,angleInit[1].split(',')),map(float,a[1].split(',')),name)
						time.sleep(10)
						recorder.stopMicrophonesRecording()
					if z[1] == 'Head':
						cmpHead = 1
			else:
				continue
	motion.setStiffnesses('Body',0.0)
				




	
