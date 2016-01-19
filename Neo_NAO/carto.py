#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import numpy as np
from subprocess import Popen, PIPE
import time


def changement(x_can,x_nao,y_can,y_nao,angle,sizeFactor):
    # x_can et y_can positions actuelles du nao dans le canevas
    # x_nao et y_nao la distance que le Nao va parcourir
    # angle orientation actuelle du naro
    # sizeFactor le rapport en pixel/metre 
    y_can = y_can + ( x_nao*np.sin(angle) + y_nao*np.cos(angle) ) * sizeFactor
    x_can = x_can + ( y_nao*np.sin(angle) + (-1)*x_nao * np.cos(angle) ) * sizeFactor
    return x_can, y_can


def CorFleche (corX,corY,theta,tailleFleche):
    # renvoie les coord de la fleche a dessiner
    # renvoie : x_debut, y_debut, x_fin, y_fin
    # tailleFleche la longueur de la fleche en pixel
    yF=tailleFleche*np.cos(theta)
    xF=tailleFleche*np.sin(theta)
    return corX,corY,corX+xF,corY+yF

#creer les image du nao et de la fleche
def frame_canv(PosX,PosY,widget,image,theta,sizeFleche):
    widget.create_image(PosX,PosY, image = image, state = NORMAL, tags = 'nao')
    xf_s,yf_s,xf_e,yf_e = CorFleche(PosX,PosY,theta,sizeFleche)
    widget.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'red', tags = 'fleche')

#methode permetant de choisir la direction vers laquelle le NAO avance
def direction(fen, canevas, x, y, theta, dx, dy, Theta, sizeFac):
    print "direction"
    #calcul des nouvelles coordonnées du NAO avec pos_act + déplacement referentiel canevas
    xx, yy=changement(x, dy, y, dx, Theta, sizeFac) 
    print x, xx
    print y, yy
    #choix du type de mouvement simple
    
    #if theta != Theta:

    if y > yy : 
        print "haut"
        theta = theta + Theta
        rotate(fen, canevas, x, y, theta, sizeFac) 
        haut(fen, canevas, x, y, xx, yy, Theta, sizeFac)
    elif y < yy:
        print "bas", dx, dy
        theta = theta + Theta
        rotate(fen, canevas, x, y, theta, sizeFac) 
        bas(fen, canevas, x, y, xx, yy, Theta, sizeFac)
    elif x > xx:
        print "gauche"
        theta = theta + Theta
        rotate(fen, canevas, x, y, theta, sizeFac) 
        gauche(fen, canevas, x, y, xx, yy, Theta, sizeFac)
    elif x < xx: 
        print "droite"
        theta = theta + Theta
        rotate(fen, canevas, x, y, theta, sizeFac) 
        droite(fen, canevas, x, y, xx, yy, Theta, sizeFac) 


    #si mouvement suivant un angle on fait
    # elif y >yy and x > xx

    
#direction gauche
def gauche(fen, canevas, x, y, xx, yy, theta, sizeFleche):
    if x > xx:
        x = x - 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        #fen.after(50, gauche)
        time.sleep(0.01)
        gauche(fen, canevas, x, y, xx, yy, theta, sizeFleche)
 
#direction droite
def droite(fen, canevas, x, y, xx, yy, theta, sizeFleche):#dx, dy, theta, tag1, tag2):
    if x < xx:        
        x = x + 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        #fen.after(50, droite)
        time.sleep(0.01)
        droite(fen, canevas, x, y, xx, yy, theta, sizeFleche)

#direction haut
def haut(fen, canevas, x, y, xx, yy, theta, sizeFleche):
    if y > yy:
        y = y - 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        #fen.after(50, haut)#dx, dy, theta, tag1, tag2))
        time.sleep(0.01)
        haut(fen, canevas, x, y, xx, yy, theta, sizeFleche)
 
#direction bas
def bas(fen, canevas, x, y, xx, yy, theta, sizeFleche):
    if y < yy:  
        y = y + 10
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        #print y 
        #fen.after(50, bas(fen, canevas, x, y, xx, yy, theta, sizeFleche))
        time.sleep(0.01)
        bas(fen, canevas, x, y, xx, yy, theta, sizeFleche)

#Rotation 
def rotate(fen, canevas, x, y, theta, sizeFleche):
    x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
    canevas.coords('nao', x, y)
    canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
    #fen.after(50, bas)#dx, dy, theta, tag1, tag2))


#initialise le canevas et la fenetre
def Init(fen, canevas, tetenao, x, y, dx, dy, nTheta):
    #creation de la fenetre    
    fen.title('animation du NAO')
    canevas.grid(row =1, column =2, rowspan =200, padx=5, pady=5)
    #affiche la tete dans la fentre
    frame_canv(x,y,canevas,tetenao,0,15)
 
      
