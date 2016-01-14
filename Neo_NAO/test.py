#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import numpy as np

def CorFleche (corX,corY,theta,tailleFleche):
    yF=tailleFleche*np.cos(theta)
    xF=tailleFleche*np.sin(theta)
    return corX,corY,corX+xF,corY+yF


def frame_canv(PosX,PosY,widget,image,theta,sizeFleche):
    widget.create_image(PosX,PosY, anchor = CENTER, image = image, state = NORMAL, tags = 'nao')
    xf_s,yf_s,xf_e,yf_e = CorFleche(PosX,PosY,theta,sizeFleche)
    widget.create_line(xf_s,yf_s,xf_e,yf_e,arrow = LAST,fill= 'orange', tags = 'fleche')

def anime():
   global x, y
   if x<=250: 
      x,y=x+1,y+0
      xf_s,yf_s,xf_e,yf_e = CorFleche(x,y,0,15)
      canevas.coords('nao',x,y)
      canevas.coords('fleche',xf_s,yf_s, xf_e, yf_e)
      fen.after(10, anime)

fen=Tk()
fen.title('animation avec tkinter')
canevas=Canvas(fen,bg='dark gray',height=600, width=1000)
canevas.pack()   
x,y=50,50
tetenao = PhotoImage(file ="naoHead.png")
frame_canv(x,y,canevas,tetenao,0,15)
anime() 

 
fen.mainloop

