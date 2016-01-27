#!/usr/bin/env python
# -*- encoding: UTF-8 -*- 

import Audio_recording
import loca
import direction
import carto
import time

import matplotlib.pyplot as plt 
from Tkinter import * 
import numpy as np

from PIL import Image
robotIP= 'nao.local'
PORT = 9559
X, Y, Theta = 0, 0, 0

def IBI():  
    global x, y, theta, X, Y, Theta, sizeFac, id_nao, id_nao_old, id_carte, Head, OldHead, carte
    #Audio_recording.record(robotIP)
    #[maxi, mean]= loca.localise()
    #X, Y, Theta = direction.moveTo(robotIP, PORT, 1)
    X, Y, Theta = 1, 0, -np.pi/2
  
    #recupère les nouvelle coordonnées du nao
    n_x, n_y, n_theta = carto.direction(canevas, x, y, theta, X, Y, Theta, sizeFac)
     
    print "theta:", theta, "ntheta:", n_theta

    #tracer de la carte polaire
    carto.cartePol(theta, n_theta)
    canevas.delete(id_carte)
    carte = carto.chargement("cartePol.png")
    id_carte = carto.frame_canv(x, y, canevas, carte, 'carte')

    #rotation de la tete du old_nao dans le bon sens
    carto.rotate("naoHeadGris.gif", "initnaoOld.gif", theta)
    canevas.delete(id_nao_old)
    OldHead = carto.chargement("naoHeadGris.gif")
    id_nao_old = carto.frame_canv(x, y, canevas, OldHead, 'old_nao')
    

    #rotation de la tete du nao dans le bon sens
    carto.rotate("naoHead.png", "initnao.png", n_theta)

    #tracer de la nouvelle tete
    canevas.delete(id_nao)
    Head = carto.chargement("naoHead.png")
    id_nao = carto.frame_canv(n_x, n_y, canevas, Head, 'nao')
    x, y, theta = n_x, n_y, n_theta



def posInit(current_name, init_name):
    #image initiale nao 
    nao = Image.open(init_name)
    filename = current_name
    nao.save(filename)
    
#remise a zero du canevas
def RAZ():
    global x, y, X, Y, Theta, theta, canevas, carte, id_nao, id_carte, Head 

    #cordonnée initial du NAO
    x,y=width/2,height/2
    X, Y, Theta, theta = 0, 0, 0, 0
  
    #recupère la bonne tete de nao
    posInit("naoHead.png", "initnao.png")
    
    #tracer Head sur le canevas
    canevas.delete(id_nao)
    canevas.delete(id_nao_old)
    canevas.delete(id_carte)

    Head = carto.chargement("naoHead.png")
    id_nao = carto.frame_canv(x, y, canevas, Head, 'nao')

def bouttons(fen, theta):   
    Button(fen, text="Exit", command=sys.exit).grid(row = 4)
    Button(fen, text="R.A.Z", command=RAZ). grid(row = 8)
    Button(fen, text="I.B.I.", command=IBI). grid(row = 12)

#parametre global
#param taille fentre
height = 700
width = 1000 
sizeFac=100

#cordonnée initial du NAo
x,y=width/2,height/2

#param taille et angle fleche 
theta = 0
sizeF = 20

#creation de la fenetre & du canevas
fen=Tk()
canevas=Canvas(fen,bg='white',height = height, width = width )
#load de la tete NAO
Head = carto.chargement("naoHead.png")
OldHead = carto.chargement ("naoHeadGris.gif")
carte = carto.chargement("cartePol.png")
#nom des objets NAO et fleche
tag1 = 'nao'
tag2 = 'fleche'
dx, dy=0, 0
id_nao, id_nao_old, id_carte = 0, 0, 0

id_nao = carto.Init(fen, canevas, Head, carte, x , y, dx, dy)
bouttons(fen, theta)

# faire vivre la fenetre
fen.mainloop() # doit etre a la fin car doit garder la main



