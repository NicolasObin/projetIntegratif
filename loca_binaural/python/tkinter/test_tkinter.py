#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk

fenetre = Tk()
fenetre['bg'] = 'white' # background de la fenetre tkinter

# frame qui contiendra du texte
frame_texte = Frame(fenetre, borderwidth=2, relief=GROOVE)
frame_texte.pack(side=TOP, padx = 5, pady = 5)

label = Label(frame_texte, text = "hello world") # un texte quelconque
label.pack()

# une autre frame pour le canvas
frame_canvas = Frame(fenetre, borderwidth=2, relief=GROOVE)
frame_canvas.pack(side=BOTTOM, padx = 5, pady = 5)
canvas = Canvas(frame_canvas, width = 1000, height = 1000, background = 'gray')

# ajout d'une image du Nao
#tetenao = PhotoImage(file='tetenao.gif')
#image = Image.open("tetenao.jpg")
#tetenao = ImageTk.PhotoImage(image)
tetenao = PhotoImage(file ="tetenao.gif") # attention si ya une instance Tkinter encore ouverte ça chie
x = 100
y = 100
canvas.create_image(x,y, anchor = CENTER, image = tetenao, state = NORMAL)
canvas.create_text(x,y-15,text = 'Pos 1', anchor = CENTER, fill = 'black')
canvas.create_line(x,y,x+25,y+50,arrow = LAST,fill= 'orange')
canvas.pack()

# faire vivre la fenetre
fenetre.mainloop()
