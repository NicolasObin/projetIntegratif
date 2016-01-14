# coding: utf8

import EEALib as ea
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np

fs, my_audio = wav.read ('/home/chaikou/Documents/Neo_NAO/audio_rec/audio_acquisition.wav')
#Separation des canaux
can1L = my_audio[:,0]
can2R = my_audio[:,1]


#fs, can1L = wav.read('wavs/droite_45_debruiteCan1.wav','r')
#fs, can2R = wav.read('wavs/droite_45_debruiteCan2.wav','r')



#print 'freq. d échantillonage : ',fs

T = 0.05		# taille de la fenêtre
hop = T			# déplacement de la fenêtre
N = int(T*fs) 	# nbre de points dans une fenêtre
c = 340.		# vitesse du son
dist = 0.135	# distance entre les micros
fmin = 100		# fréquence minimale pour l'IPD
fmax = 1000		# fréquence maximale pour l'IPD

# calcul de la FFT
stft1L = ea.stft(can1L,fs,T,hop)
stft2R = ea.stft(can2R,fs,T,hop)
fbins = np.fft.fftfreq(N,1./fs)		# bins fréquentiels

# on vire la partie symetrique (signal réel)
L = stft1L.shape[1]/2
stft1L = stft1L[:,:L]
stft2R = stft2R[:,:L]
fbins = fbins[:L]
#print fbins.shape, fbins

# on attrape le max de chaque trame
max1L = np.max(abs(stft1L),axis=1)
topmax1L = np.max(abs(stft1L))
arg1L = np.argmax(abs(stft1L),axis=1)
max2R = np.max(abs(stft2R),axis=1)
topmax2R = np.max(abs(stft2R))
arg2R = np.argmax(abs(stft2R),axis=1)
#print 'Pic canal 1L : ',max1L,' @ ', arg1L
#print 'Pic canal 2R : ',max2R,' @ ', arg2R

if topmax1L > topmax2R:
	flag = 1
	ILD =  'tu es sur ma gauche'
else:
	flag = 0
	ILD = 'tu es sur ma droite'

print ILD
return flag

## plot stft
#plt.figure(1)
#plt.title('STFT can1L')
#plt.imshow(abs(stft1L).T,cmap='jet',aspect='auto',origin='lower')
#plt.figure(2)
#plt.title('STFT can2R')
#plt.imshow(abs(stft2R).T,aspect='auto',origin='lower')
#plt.show()
"""
# on ne va calculer l'angle que pour les max ayant la meme frequence
angle_est_liste = []
for ii in np.arange(0,arg1L.shape[0]):
	if arg1L[ii] == arg2R[ii]:
		if (fbins[arg1L[ii]] > fmin) & (fbins[arg1L[ii]] < fmax):
			print 'fbin ',fbins[arg1L[ii]]
			delta = np.angle(stft1L[ii,arg1L[ii]]) - np.angle(stft2R[ii,arg2R[ii]])
			aeg = np.complex64( (c*delta) / (6.282*fbins[arg1L[ii]]*dist) )
			angle_est = np.real( np.arccos( aeg ) / 3.14 * 180 )
			angle_est_liste.append(angle_est)
			print 'delta; angle : ',delta,'; ',angle_est

print 'angle moyen : ',np.mean(angle_est_liste) # pas représentatif
"""
