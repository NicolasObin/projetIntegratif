#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import numpy as np
from subprocess import Popen, PIPE


def pointe():  
    process = Popen("python pointe.py", shell=True, stderr=PIPE)


def bouttons():   
    Button(fen, text="Exit", command=sys.exit).grid(row =4)
    Button(fen, text="Pointe", command=pointe). grid(row =6)

    


def bouttonLoca2():
    #canevas = Tkinter.Button(None)
    b = Button(fen, text="Localisation 2", command=sys.exit)
    b.pack(side = BOTTOM)

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
def direction(dx, dy, Theta):
    print "direction"
    global x, y, xx, yy, theta
    #calcul des nouvelles coordonnées du NAO avec pos_act + déplacement referentiel canevas
    xx, yy=changement(x, dy, y, dx, theta, sizeFac) 
    print x, xx
    print y, yy
    #choix du type de mouvement simple
  
    if y > yy : 
        print "haut"
        haut()
    elif y < yy:
        print "bas", dx, dy
        bas()
    elif x > xx:
        print "gauche"
        gauche()
    elif x < xx: 
        print "droite"
        droite() 
    elif theta != Theta:
        theta = theta + Theta
        print "rotate", theta
        rotate() 

    #si mouvement suivant un angle on fait
    # elif y >yy and x > xx

    
#direction gauche
def gauche():#dx, dy, theta, tag1, tag2):
    global x, y, xx, yy 
    if x > xx:

        x = x - 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        fen.after(50, gauche)#dx, dy, theta, tag1, tag2))
 
#direction droite
def droite():#dx, dy, theta, tag1, tag2):
    global x, y, xx, yy 
    if x < xx:        
        x = x + 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        fen.after(50, droite)#dx, dy, theta, tag1, tag2))

#direction haut
def haut():#dx, dy, theta, tag1, tag2):
    global x, y, xx, yy 
    if y > yy:
        y = y - 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        fen.after(50, haut)#dx, dy, theta, tag1, tag2))
 
#direction bas
def bas():#dx, dy, theta, tag1, tag2):
    global x, y, xx, yy 
    print y, yy
    if y < yy:  
        print "if"      
        y = y + 1
        x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
        canevas.coords('nao', x, y)
        canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
        fen.after(50, bas)#dx, dy, theta, tag1, tag2))

#Rotation 
def rotate_d():
    global x, y, theta
    x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
    canevas.coords('nao', x, y)
    canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
    #fen.after(50, bas)#dx, dy, theta, tag1, tag2))

#Rotation 
def rotate_g():
    global x, y, theta
    x_deb, y_deb, x_fin, y_fin = CorFleche(x, y, theta,sizeFleche)
    canevas.coords('nao', x, y)
    canevas.coords('fleche', x_deb, y_deb, x_fin, y_fin)
    #fen.after(50, bas)#dx, dy, theta, tag1, tag2))

#initialise le canevas et la fenetre
def Init():
    #creation de la fenetre
    global fen, canevas,tetenao
    bouttons()    
    fen.title('animation du NAO')
    canevas.grid(row =1, column =2, rowspan =200, padx=5, pady=5)
    #affiche la tete dans la fentre
    frame_canv(x,y,canevas,tetenao,0,15)
    nTheta = 0
    #print  theta
    direction(dx, dy, nTheta)    
    # faire vivre la fenetre
    fen.mainloop() # doit etre a la fin car doit garder la main
      
#angle = np.pi/2
#parametre global
#param taille fentre
height=700
width=1000 
sizeFac=100
#cordonnée initial du NAo
x,y=width/2,height/2
#première cordonnée sur le canvas
xx, yy=changement(x, 0, y, 0, 0, sizeFac) 
theta = 0
#param fleche
sizeFleche = 20
#creation de la fenetre & du canevas
fen=Tk()
canevas=Canvas(fen,bg='dark grey',height = height, width = width )
#load de la tete NAO
tetenao = PhotoImage(file ="naoHead.png")
#nom des objets NAO et fleche
tag1 = 'nao'
tag2 = 'fleche'
dx, dy=1 ,0
Init()

