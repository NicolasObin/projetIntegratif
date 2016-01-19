#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

"""
from Audio_recording import *
from loca import *
from direction import *
from carto import *
"""
import Audio_recording
import loca
import direction
import carto

from Tkinter import * 
import numpy as np

robotIP= 'nao.local'
PORT = 9559
X, Y, Theta = 0, 0, 0

def pointe():  
    global X, Y, Theta
    Audio_recording.record(robotIP)
    [maxi, mean]= loca.localise()
    X, Y, Theta = direction.moveTo(robotIP, PORT, mean)
    carto.direction(fen, canevas, x, y, theta, X, Y, Theta, sizeFac)
    print "toto", X, Y, theta

def bouttons(fen):   
    Button(fen, text="Exit", command=sys.exit).grid(row =4)
    Button(fen, text="Pointe", command=pointe). grid(row =6)


#def localisation

#parametre global
#param taille fentre
height=700
width=1000 
sizeFac=1000
#cordonnée initial du NAo
x,y=width/2,height/2

#première cordonnée sur le canvas
xx, yy=carto.changement(x, 0, y, 0, 0, sizeFac)
 

#param taille et angle fleche 
theta = 0
sizeFleche = 20


#creation de la fenetre & du canevas
fen=Tk()
canevas=Canvas(fen,bg='dark grey',height = height, width = width )
#load de la tete NAO
tetenao = PhotoImage(file ="naoHead.png")
#nom des objets NAO et fleche
tag1 = 'nao'
tag2 = 'fleche'
dx, dy=0 ,0

carto.Init(fen, canevas, tetenao, x , y, dx, dy, theta)
bouttons(fen)
#print "toto", X, Y, theta

# faire vivre la fenetre
fen.mainloop() # doit etre a la fin car doit garder la main
      


