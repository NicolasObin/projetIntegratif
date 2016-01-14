# coding: utf8

import EEALib as ea
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np

def localise():

    fs, my_audio = wav.read ('/home/chaikou/Documents/Neo_NAO/audio_rec/audio_acquisition.wav')
    #Separation des canaux
    can1L = my_audio[:,0]
    can2R = my_audio[:,1]

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

    # on vire la partie symetrique (signal réel)
    L = stft1L.shape[1]/2
    stft1L = stft1L[:,5:L]
    stft2R = stft2R[:,5:L]

    # on attrape le max de chaque trame
    topmax1L = np.max(abs(stft1L))
    topmax2R = np.max(abs(stft2R))
    m1L = np.mean(abs(stft1L))
    m2R = np.mean(abs(stft2R))


    if topmax1L > topmax2R:
	    flag_max = 1
	    ILD_max =  'max -> gauche'
    else:
	    flag_max = 0
	    ILD_max = 'max ->droite'

    if m1L > m2R:
	    flag = 1
	    ILD =  'mean -> gauche'
    else:
	    flag = 0
	    ILD = 'mean -> droite'

    print ILD_max, ILD
    return [flag_max, flag]


