#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import sys
import motion
import time
from naoqi import ALProxy
import numpy as np

#Centré l'image au début PARAMETRES INITIAUX
can_width = 1000
can_height = 600
sizeFac=1000
sizeFleche = 15
theta = 0

# CREATION FENETRE TKINTER
fenetre = Tk()
fenetre['bg'] = 'darkgray' # background de la fenetre tkinter

# une autre frame pour le canvas
#frame_canvas = Frame(fenetre, borderwidth=2, relief=GROOVE)
#frame_canvas.pack(side=BOTTOM, padx = 5, pady = 5)
canvas = Canvas(fenetre, width = can_width, height = can_height, background = 'darkgray')
canvas.pack()

    
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

def frame_canv(PosX,PosY,widget,image,theta,sizeFleche):
    widget.create_image(PosX,PosY, anchor = CENTER, image = image, state = NORMAL, tags = 'nao')
    xf_s,yf_s,xf_e,yf_e = CorFleche(PosX,PosY,theta,sizeFleche)
    widget.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange', tags = 'fleche')


def initFenetre(corX, corY):

    # image nao    
    tetenao = PhotoImage(file ="naoHead.png") # attention si ya une instance Tkinter encore ouverte ça chie
     #Position initiale 
    frame_canv(corX,corY,canvas,tetenao,theta,sizeFleche)
    fenetre.mainloop() # doit etre a la fin car doit garder la main


def anime():
   corx=100
   cory=100
   if corx<=1000:
      corx=corx+10
      canvas.coords('nao',corx,cory)
      fenetre.after(10, anime)
      

"""
def Marcher(X, Y, corX, corY):
    xx,yy = changement(corX,X,corY,Y,theta,sizeFac)
    animeX(xx, corX, corY)
  """

def main(robotIP):
    
    corX = 200#can_width/2
    corY = 200#can_height/2
    initFenetre(corX, corY)

    anime()    

    """
    # 1ER DEPLACEMENT
	# created a walk task
    x = 0.2
    y = 0
    theta_goal = 0
    motionProxy.post.moveTo(x, y, theta_goal)
	# wait that the move process start running
    time.sleep(0.1)

    #Position initiale
    frame_canv(corX,corY,'P0',canvas,tetenao,theta,sizeFleche)
    xx,yy = changement(corX,x,corY,y,theta,sizeFac)
    
    # update des param
    corX = xx
    corY = yy
    theta = theta + theta_goal

    #Position finale
    frame_canv(xx,yy,'P1',canvas,tetenao,theta,sizeFleche)
    #canvas.tag_lower(objet) mettre en arriére plan
    canvas.tag_lower(canvas.create_rectangle(can_width, can_height, xx, yy, fill="orange"))
    canvas.pack()
    fenetre.update()

    # faire vivre la fenetre Tkinter"""


if __name__ == "__main__":
    robotIp = 'nao.local'

    if len(sys.argv) <= 1:
        print "Usage python Cartographie.py robotIP (optional default: nao.local)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
