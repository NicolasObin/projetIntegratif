# coding: utf8
import scipy, numpy as np
import scipy.io.wavfile as wav
import EAALib as eaa
import math

##CONSTANTE
c=340 #Vitesse du son dans l'air
d=0.135 #Distance interbinaural

#Parametre
T = 0.2 #Taille de la fenetre de la stft
hop = 0.2 #Taille du pas de la stft

#Signal de quatre canaux
fs, gauche = wav.read('1.wav')
fs, droite = wav.read('2.wav')

#Separation des canaux
#gauche = my_audio[:,0]
#droite = my_audio[:,1]
#avant = my_audio[:,2]
#arriere = my_audio[:,3]

#Transforme stft
#stft_gauche = eaa.stft(gauche,fs,T,hop)
#stft_droite = eaa.stft(droite,fs,T,hop)
#stft_avant = eaa.stft(avant,fs,T,hop)
#stft_arriere = eaa.stft(arriere,fs,T,hop)
fft_gauche = np.fft.fft(gauche)
fft_droite = np.fft.fft(droite)


r = eaa.compute_angle(fft_gauche, fft_droite , 48000 , c, d)
print(r)
