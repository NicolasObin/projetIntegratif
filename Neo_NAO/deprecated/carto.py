#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import numpy as np
from subprocess import Popen, PIPE
import time

from PIL import Image



def changement(x_can,x_nao,y_can,y_nao,angle,sizeFactor):
    # x_can et y_can positions actuelles du nao dans le canevas
    # x_nao et y_nao la distance que le Nao va parcourir
    # angle orientation actuelle du naro
    # sizeFactor le rapport en pixel/metre 
    """    
    y_can = y_can + ( (-1)*x_nao*np.sin(angle) + y_nao*np.cos(angle) ) * sizeFactor
    x_can = x_can + ( y_nao*np.sin(angle) + x_nao * np.cos(angle) ) * sizeFactor
    return x_can, y_can
    """
    x_can = x_can + ( x_nao*np.sin(angle) + y_nao*np.cos(angle) ) * sizeFactor
    y_can = y_can + ( (-1)*y_nao*np.sin(angle) + x_nao * np.cos(angle) ) * sizeFactor
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
def direction(fen, canevas, x, y, theta, dx, dy, new_theta, sizeConv, sizeF):
    print "carto_direction"
    #calcul des nouvelles coordonnées du NAO avec pos_act + déplacement referentiel canevas
    
    theta = theta+ new_theta    
    xx, yy=changement(x, dx, y, dy, theta, sizeConv)

    print "x:", x, ", xx:", xx
    print "y:", y, ", yy:", yy
    print "theta:", theta, "new_theta:", new_theta   
    #choix du type de mouvement simple
    
    #if theta != Theta:
    if y != yy :
        if y > yy : 
            print "carto_haut"
            rotate(fen, canevas, x, y, theta, sizeF) 
            haut(fen, canevas, x, y, xx, yy, theta, sizeF)
        elif y < yy:
            print "carto_bas"
            rotate(fen, canevas, x, y, theta, sizeF) 
            bas(fen, canevas, x, y, xx, yy, theta, sizeF)
    
    if x != xx:
        if x > xx:
            print "carto_droite"
            rotate(fen, canevas, x, y, theta, sizeF) 
            gauche(fen, canevas, x, y, xx, yy, theta, sizeF)
        elif x < xx: 
            print "carto_gauche"
            rotate(fen, canevas, x, y, theta, sizeF) 
            droite(fen, canevas, x, y, xx, yy, theta, sizeF) 

    return xx, yy, theta
    #si mouvement suivant un angle on fait
    # elif y >yy and x > xx

    
#direction gauche
def gauche(fen, canevas, x, y, xx, yy, theta, sizeFleche):

    #x_deb, y_deb, x_fin, y_fin = CorFleche(xx, yy, theta,sizeFleche)
    canevas.coords('pol', xx, yy)
    canevas.coords('nao', xx, yy)
    #canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
    """
    if x > xx:
        x = x - 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        #fen.after(50, gauche)
        time.sleep(0.01)
        gauche(fen, canevas, x, y, xx, yy, theta, sizeFleche)
    """
#direction droite
def droite(fen, canevas, x, y, xx, yy, theta, sizeFleche):

    #x_deb, y_deb, x_fin, y_fin = CorFleche(xx, yy, theta,sizeFleche)
    canevas.coords('pol', xx, yy)
    canevas.coords('nao', xx, yy)
    #canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)

#direction haut
def haut(fen, canevas, x, y, xx, yy, theta, sizeFleche):
    #x_deb, y_deb, x_fin, y_fin = CorFleche(xx, yy, theta,sizeFleche)
    canevas.coords('pol', xx, yy)
    canevas.coords('nao', xx, yy)
    #canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)

#direction bas
def bas(fen, canevas, x, y, xx, yy, theta, sizeFleche):
    #x_deb, y_deb, x_fin, y_fin = CorFleche(xx, yy, theta,sizeFleche)
    canevas.coords('pol', xx, yy)
    canevas.coords('nao', xx, yy)
    #canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)

#Rotation 
def rotate(fen, canevas, x, y, theta, naoHead, pol):

	# rotate de theta en degrees
    imRotate = naoHead.rotate(theta*180/np.pi)
    filename = "naoHead.png"
    imRotate.save(filename)
    
	# rotate de theta en degrees
    imRotate = pol.rotate(theta*180/np.pi)
    filename = "carte.png"
    imRotate.save(filename)
    
    x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
    #canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
    

#initialise le canevas et la fenetre
def Init(fen, canevas, tetenao, carte, x, y, dx, dy):
    #creation de la fenetre    
    fen.title('animation du NAO')
    canevas.grid(row =1, column =2, rowspan =200, padx=5, pady=5)
    #affiche la tete dans la fentre
    frame_canv(x,y,canevas,carte,0,15)
    frame_canv(x,y,canevas,tetenao,0,15)

 
      
