#!/usr/bin/env python
# coding=utf-8

# implémentation python de la version de localisation naïve proposée par Laurent
# se basant uniquement sur le ILD

import numpy as np
import scipy.io.wavfile as wav
import EAALib as eea
import matplotlib.pyplot as plt
from time import sleep
from scipy import fftpack

############# parametres ###############################
N = 2048                    # nbre de points pour la TF
hop = N/2                   # chevauchement de 50%
pmod = [-2, -1, 0, 1, 2]    # modulo 2*pi*p pour l'ITD
c = 340                     # célérité du son
r = 0.06                    # rayon de la tête
########################################################

def approx(x): # approximation de sin(x)+x
    return 0.50018*x + 0.009897*(x**3) + 0.00093*(x**5)

# chargement des signaux
fs, sig = wav.read('wavs/continu/gauche.wav')
gauche = sig[:,0]
droite = sig[:,1]
print 'canaux audio chargés, tailles : ',gauche.shape,droite.shape

# calcul TFCT
fbins = fftpack.fftfreq(N,d=1./fs)[0:N/2]
Xd = eea.stft(droite,N,hop).T[0:N/2,:]
Xg = eea.stft(gauche,N,hop).T[0:N/2,:]

# matrice inter aurale
Minter = Xd/Xg

# indices inter auraux et angles associes
ILD = 20*np.log10(np.abs(Minter))
theta_L = np.arcsin(ILD)
ITD = np.zeros(shape=(len(fbins),ILD.shape[1],len(pmod)))
theta_T = np.zeros(shape=(len(fbins),ILD.shape[1],len(pmod)))
for f in np.arange(0,len(fbins)):
    for n in np.arange(0,ILD.shape[1]):
        for p in np.arange(0,len(pmod)):
            ITD[f,n,p] = (1./(6.183*fbins[f]))*(np.angle(Minter[f,n])+(2*np.pi*pmod[p]))
            theta_T[f,n,p] = approx(c*ITD[f,n,p]/r)

# estimation de theta
theta = np.zeros(shape=(len(fbins),ILD.shape[1]))
for f in np.arange(0,len(fbins)):
    for n in np.arange(0,ILD.shape[1]):
        min_dev = 99999
        best_p = np.nan
        for p in np.arange(0,len(pmod)):
            val = np.abs(theta_L[f,n]-theta_T[f,n,p])
            if val < min_dev:
                # print "best p : ", p
                best_p = p
                min_dev = val
        # print "is p a nan ? ",np.isnan(best_p)
        if np.isnan(best_p):
            theta[f,n] = np.nan
        else:
            theta[f,n] = theta_T[f,n,best_p]

# vote pour chaque trame
nbins = 36
table_vote = np.zeros(shape=(nbins,ILD.shape[1]))
angle_vote = np.zeros(shape=(0))
for n in np.arange(0,ILD.shape[1]):
    azimuths = np.zeros(shape=(0))
    for f in np.arange(0,len(fbins)):
        if not(np.isnan(theta[f,n])):
            azimuths = np.append(azimuths,theta[f,n]*180/np.pi)
    #         # print azimuths
    #         # print theta[f,n]*180/np.pi
    # if azimuths.size > 0:
    #     print azimuths
    print azimuths.size
    hist, anglesbins = np.histogram(azimuths,bins=nbins,range=(-180,180))
    table_vote[:,n] = hist
    angle_vote = np.append(angle_vote,anglesbins[np.argmax(hist)])
# plot
plt.figure(0)
plt.title('Azimuth estime pour chaque trame')
plt.plot(angle_vote.tolist(),'ro')
plt.show()
# plot
# plt.figure(0)
# plt.title('Spectrogramme droit')
# plt.imshow(np.abs(Xd), aspect = 'auto', origin = 'lower')
# plt.figure(1)
# plt.title('Spectrogramme gauche')
# plt.imshow(np.abs(Xg), aspect = 'auto', origin = 'lower')
# plt.figure(2)
# plt.imshow(np.abs(ILD),aspect = 'auto', origin = 'lower')
# plt.title('Matrice interaurale')
# plt.figure(3)
# plt.title('Azimuth')
# plt.imshow(np.real(azimuth),aspect='auto', origin = 'lower')
# plt.show()

# for ii in np.arange(1,azimuth.shape[1]):
#     plt.figure(4)
#     plt.title('Azimuth angle')
#     plt.plot(np.real(azimuth.reshape(-1)[(ii-1)*M:ii*M-1])*180/np.pi,'ro')
#     plt.show()
# for ii in np.arange(1,azimuth.shape[0]):
#     plt.figure(4)
#     plt.title('Azimuth angle')
#     plt.plot(np.real(azimuth[ii,:])*180/np.pi,'ro')
#     plt.show()
