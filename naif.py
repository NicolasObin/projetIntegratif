#!/usr/bin/env python
# coding=utf-8

# implémentation python de la version de localisation naïve proposée par Laurent
# se basant uniquement sur le ILD

import numpy as np
import scipy.io.wavfile as wav
import EAALib as eea
import matplotlib.pyplot as plt
from time import sleep
from scipy import fftpack, signal

############# PARAMETRES ###############################
N = 2048                                # nbre de points pour la TF
hop = N/2                               # chevauchement de 50%
pmod = [-4, -3, -2, -1, 0, 1, 2, 3, 4]  # modulo 2*pi*p pour l'ITD
c = 340                                 # célérité du son
r = 0.0606                              # rayon de la tête
ntrames = 50                            # nbre de trames cumulées
fmax = 180                              # numero de bin max freq
########################################################

def approx(x): # approximation de sin(x)+x
    return 0.50018*x + 0.009897*(x**3) + 0.00093*(x**5)

# chargement des signaux
fs, sig = wav.read('wavs/nicolas/droite.wav')
gauche = sig[:,0]
droite = sig[:,1]
print 'canaux audio chargés, tailles : ',gauche.shape,droite.shape

# FILTRAGE PASSE BAS A 4000Hz
FC = 0.05/(0.5*fs)                                   # cutoff freq 4000 Hz
N = 1001                                             # number of filter taps
a = 1                                                # filter denominator
b = signal.firwin(N, cutoff=FC, window='hamming')    # filter numerator
gauche = signal.lfilter(b, a, gauche)                # filtered output
droite = signal.lfilter(b, a, droite)

# TRANSFORMEE DE FOURIER A COURT TERME
fbins = fftpack.fftfreq(N,d=1./fs)[0:N/2]   # points frequentiels
Xd = eea.stft(droite,N,hop).T[0:N/2,:]      # TFCT
Xg = eea.stft(gauche,N,hop).T[0:N/2,:]
Minter = Xd/Xg                              # matrice interaurale

# INDICES INTERAURAUX ET ANGLES ESTIMES
ILD = 20*np.log10(np.abs(Minter))
theta_L = np.arctan(ILD)
ITD = np.zeros(shape=(len(fbins),ILD.shape[1],len(pmod)))
theta_T = np.zeros(shape=(len(fbins),ILD.shape[1],len(pmod)))
for f in np.arange(0,len(fbins)):
    for n in np.arange(0,ILD.shape[1]):
        for p in np.arange(0,len(pmod)):
            ITD[f,n,p] = (1./(2*np.pi*fbins[f]))*(np.angle(Minter[f,n])+(2*np.pi*pmod[p]))
            theta_T[f,n,p] = approx(c*ITD[f,n,p]/r)

# estimation de theta à partir de theta_T et theta_L
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

# construction de l'histogramme de vote et de la pondération
nbins = 36
table_vote = np.zeros(shape=(nbins,ILD.shape[1]))
poids_vote = np.zeros(shape=(nbins,ILD.shape[1]))
for n in np.arange(0,ILD.shape[1]):
    azimuths = np.zeros(shape=(0))
    ponderations = np.zeros(shape=(0))
    for f in np.arange(0,len(fbins)):
        if not(np.isnan(theta[f,n])):
            azimuths = np.append(azimuths,theta[f,n]*180/np.pi)
            ponderations = np.append(ponderations,np.abs(Xd[f,n])+np.abs(Xg[f,n]))
    #         # print azimuths
    #         # print theta[f,n]*180/np.pi
    # if azimuths.size > 0:
    #     print azimuths
    # print azimuths.size

    # Histogramme des azimuths sur -180:10:180
    hist, anglesbins = np.histogram(azimuths,bins=nbins,range=(-180,180))
    table_vote[:,n] = hist
    # Et le vecteur de poids qui va avec
    # récupération des indices correspondants aux bins grâce à np.digitize
    inds = np.digitize(azimuths,anglesbins[1:-1])
    ponderations = ponderations / float(np.sum(ponderations)) # normalisation
    poids = np.zeros(shape=(hist.shape[0]))
    for t in np.arange(0,inds.shape[0]):
        # on accumule les poids pour chaque angle discrétisé
        poids[inds[t]] = poids[inds[t]] + ponderations[t]
    poids_vote[:,n] = poids

# vote pour une trame
angle_vote_1 = np.zeros(shape=(0))
angle_vote_1_nopond = np.zeros(shape=(0))
for n in np.arange(0,ILD.shape[1]):
    # pondéré
    angle_vote_1 = np.append(angle_vote_1,anglesbins[np.argmax(table_vote[:,n]*poids_vote[:,n])])
    # non pondéré
    angle_vote_1_nopond = np.append(angle_vote_1_nopond,anglesbins[np.argmax(table_vote[:,n]*poids_vote[:,n])])

# on veut aussi un vote sur plusieurs trames successives
angle_vote_multi = np.zeros(shape=(0))
angle_vote_multi_nopond = np.zeros(shape=(0))
for n in np.arange(0,ILD.shape[1]-ntrames):
    # pondéré
    votes = table_vote[:,n:n+ntrames]*poids_vote[:,n:n+ntrames]
    votes = np.sum(votes,1) # histogramme pondéré sur les ntrames trames
    angle_vote_multi = np.append(angle_vote_multi,anglesbins[np.argmax(votes)])
    # non pondéré
    votes = table_vote[:,n:n+ntrames]
    votes = np.sum(votes,1) # histogramme pondéré sur les ntrames trames
    angle_vote_multi_nopond = np.append(angle_vote_multi_nopond,anglesbins[np.argmax(votes)])

# plot
plt.figure(0)
plt.title('Azimuth estime pour chaque trame (pond)')
plt.plot(angle_vote_1,'ro')
plt.ylim(-200,200)
plt.figure(1)
plt.title('Azimuth estime pour n trames (pond)')
plt.plot(angle_vote_multi,'ro')
plt.ylim(-200,200)
plt.figure(2)
plt.title('Azimuth estime pour chaque trame')
plt.plot(angle_vote_1_nopond,'ro')
plt.ylim(-200,200)
plt.figure(3)
plt.title('Azimuth estime pour n trames')
plt.plot(angle_vote_multi_nopond,'ro')
plt.ylim(-200,200)
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
