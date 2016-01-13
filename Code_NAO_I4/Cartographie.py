#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import sys
import motion
import time
from naoqi import ALProxy
import numpy as np

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def changement(x_can,x_nao,y_can,y_nao,angle,sizeFactor):
    x_can = x_can + ( x_nao*np.sin(angle) + y_nao*np.cos(angle) ) * sizeFactor
    y_can = y_can + ( (-1)*y_nao*np.sin(angle) + x_nao * np.cos(angle) ) * sizeFactor
    return x_can, y_can

def CorFleche (corX,corY,theta,tailleFleche):
    yF=tailleFleche*np.cos(theta)
    xF=tailleFleche*np.sin(theta)
    return corX,corY,corX+xF,corY+yF

def main(robotIP):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

	#Centré l'image au début PARAMETRES INITIAUX
    can_width = 1000
    can_height = 600
    corX = can_width/2
    corY = can_height/2
    sizeFac=1000
    sizeFleche = 15
    theta = 0
    
    # CREATION FENETRE TKINTER
    fenetre = Tk()
    fenetre['bg'] = 'white' # background de la fenetre tkinter
	# frame qui contiendra du texte
    frame_texte = Frame(fenetre, borderwidth=2, relief=GROOVE)
    frame_texte.pack(side=TOP, padx = 5, pady = 5)
    label = Label(frame_texte, text = "Déplacement sur une carte") # un texte quelconque
    label.pack()
	# une autre frame pour le canvas
    frame_canvas = Frame(fenetre, borderwidth=2, relief=GROOVE)
    frame_canvas.pack(side=BOTTOM, padx = 5, pady = 5)
    canvas = Canvas(frame_canvas, width = can_width, height = can_height, background = 'gray')
    canvas.pack()
    # image nao    
    tetenao = PhotoImage(file ="naoHead.png") # attention si ya une instance Tkinter encore ouverte ça chie

    
    # 1ER DEPLACEMENT
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
	# created a walk task
    x = 0
    y = 0.2
    theta_goal = 0

    motionProxy.moveInit()
    motionProxy.post.moveTo(x, y, theta_goal)
	# wait that the move process start running
    time.sleep(0.1)

    #Position initiale
    canvas.create_image(corX,corY, anchor = CENTER, image = tetenao, state = NORMAL, tags = 'nao')
    canvas.create_text(corX,corY-10,text = 'P0', anchor = CENTER, fill = 'red')
    xf_s,yf_s,xf_e,yf_e = CorFleche(corX,corY,theta,sizeFleche)
    canvas.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange')

    xx,yy = changement(corX,x,corY,y,theta,sizeFac)
    # update des param
    corX = xx
    corY = yy
    theta = theta + theta_goal

    #Position finale
    canvas.create_image(xx,yy, anchor = CENTER, image = tetenao, state = NORMAL)
    canvas.create_text(xx,yy-10,text = 'P1', anchor = CENTER, fill = 'red')
    xf_s,yf_s,xf_e,yf_e = CorFleche(corX,corY,theta,sizeFleche)
    canvas.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange')
    canvas.pack()
    fenetre.update()

    # 2E DEPLACEMENT
        # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
	# created a walk task
    x = 0
    y = 0
    theta_goal = -np.pi/2

    motionProxy.moveInit()
    motionProxy.post.moveTo(x, y, theta_goal)

	# wait that the move process start running
    time.sleep(0.1)
    #Position initiale
    canvas.create_image(corX,corY, anchor = CENTER, image = tetenao, state = NORMAL, tags = 'nao')
    canvas.create_text(corX,corY-10,text = 'P0', anchor = CENTER, fill = 'red')
    xf_s,yf_s,xf_e,yf_e = CorFleche(corX,corY,theta,sizeFleche)
    canvas.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange')

    xx,yy = changement(corX,x,corY,y,theta,sizeFac)
    # update des param
    corX = xx
    corY = yy
    theta = theta + theta_goal

    #Position finale
    canvas.create_image(xx,yy, anchor = CENTER, image = tetenao, state = NORMAL)
    canvas.create_text(xx,yy-10,text = 'P1', anchor = CENTER, fill = 'red')
    xf_s,yf_s,xf_e,yf_e = CorFleche(corX,corY,theta,sizeFleche)
    canvas.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange')
    canvas.pack()
    fenetre.update()

    # faire vivre la fenetre
    fenetre.mainloop() # doit etre a la fin car doit garder la main

if __name__ == "__main__":
    robotIp = 'nao.local'

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: nao.local)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
