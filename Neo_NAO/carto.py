#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import matplotlib.pyplot as plt
import numpy as np
from subprocess import Popen, PIPE
import time

from PIL import Image


def chargement(img):
    return PhotoImage(file = img)
#

def cartePol(o_theta, theta):
    toto = o_theta - np.pi/2
    #Creation du cercle
    theta = theta - o_theta
    fig = plt.figure(figsize=(2, 2)) 
    plt.subplot(1, 1, 1, projection='polar')

    #theta=y, 2:x, 3:???, 4:taille de la fleche , alpha:intensite 
    #tracer la fleche
    plt.arrow(theta, 0, 0, 0.5, alpha =1, width = 0.017,edgecolor = 'blue')
    #colorer la zone 
    plt.bar(theta-np.pi/2, 1, width= np.pi, bottom=0.0,color='red',edgecolor = 'blue')

    #save figure
    plt.savefig("carte.png")
    rotate ("cartePol.png", "carte.png", toto)
    
    



def changement(x_can,x_nao,y_can,y_nao,angle,sizeFactor):
    # x_can et y_can positions actuelles du nao dans le canevas
    # x_nao et y_nao la distance que le Nao va parcourir
    # angle orientation actuelle du naro
    # sizeFactor le rapport en pixel/metre 
    x_can = x_can + ( x_nao*np.sin(angle) + y_nao*np.cos(angle) ) * sizeFactor
    y_can = y_can + ( (-1)*y_nao*np.sin(angle) + x_nao * np.cos(angle) ) * sizeFactor
    return x_can, y_can

#creer les image du nao et de la fleche
def frame_canv(PosX, PosY, widget, img1, tag1,):
    id_nao = widget.create_image(PosX,PosY, image = img1, state = NORMAL, tags = tag1) 
    return id_nao

#methode permetant de choisir la direction vers laquelle le NAO avance
def direction(canevas, x, y, theta, dx, dy, new_theta, sizeConv):
    print "carto_direction"

#calcul des nouvelles coordonnées du NAO avec pos_act + déplacement referentiel canevas 
    print "theta:", theta, "new_theta:", new_theta  
    theta = theta+ new_theta    

    #conversion dans le repère du canevas
    xx, yy=changement(x, dx, y, dy, theta, sizeConv)
    print "x:", x, ", xx:", xx
    print "y:", y, ", yy:", yy
   
    return xx, yy, theta
 
#Rotation 
def rotate(current_name, init_name, theta):    
	# rotate nao de theta en degrees
    nao = Image.open(init_name)
    imRotate = nao.rotate(theta*180/np.pi)
    filename = current_name
    imRotate.save(filename)
   

#initialise le canevas et la fenetre
def Init(fen, canevas, nao, carte, x, y, dx, dy):
    #creation de la fenetre    
    fen.title('animation du NAO')
    canevas.grid(row =1, column =2, rowspan =200, padx=5, pady=5)
    #affiche la tete dans la fentre
    id_nao = frame_canv(x,y,canevas, nao, 'nao')
    return id_nao


 
      
