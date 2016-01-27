# coding: utf8
#le nao pointe dans la direction avec la plus grande puissance recu


import Audio_recording
import loca
import direction

robotIP= 'nao.local'
PORT = 9559

Audio_recording.record(robotIP)
#[maxi, mean]= loca.localise()
#X, Y, Theta = direction.moveTo(robotIP, PORT, mean)


