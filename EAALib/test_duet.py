# coding: utf8
import scipy, numpy as np
import scipy.io.wavfile as wav
import scipy.ndimage
import EAALib as eaa
import matplotlib.pyplot as plt

### Code DUET
## Preparation de l'audio
#Signal stereo
fs, data = wav.read('1.wav')

#Séparation des canaux
canal0=data[:,0]
canal1=data[:,1]

#%% PARAMETRES %%
N = 1024;  #Taille de fenetre STFT
hop = 512; #Taille du saut STFT

##Paramètre de l'histogramme DUET
#Pondération (Par défaut)
p=1
q=0

#Limites pour alpha, delta dans l'histogramme DUET (Par défaut)
maxa=1;
maxd=4;

#Nombre de bin pour alpha et delta dans l'histogramme DUET
abins=500;
dbins=1000;

#on definit un pic comme étant supérieur à 7/10 du pic max
rejet_max_pic=7/10

#on rejet un point de la STFT s'il ne fait pas au moins 1/100 du score max
rejet_max_score=1/1000

#Appelle a la fonction qui calcul DUET ou canal0 et canal1 sont les signaux temporels du signal les reste correspond aux paramètres définit ci-dessus
c0_stft_synth_sorted_array, c1_stft_synth_sorted_array, numsources = eaa.compDuet(canal0,canal1,N,hop,p,q,maxa,maxd,abins,dbins,rejet_max_pic,rejet_max_score)
#La fonction retourne les matrices STFT des sources séparés (1 matrice par canal).
#La matrice est une matrice 3D ou la profondeur définit le nombre de sources tandis que la matrice 2D (lignes, colonnes) représente une STFT d'une source.
#numsources indique le nombre de source séparé

##Ecriture
for i in range(0,numsources) :    
    #Retour dans le domaine temporelle 
    canal0_synth=np.int16(eaa.istft(c0_stft_synth_sorted_array[:,:,i],hop));
    canal1_synth=np.int16(eaa.istft(c1_stft_synth_sorted_array[:,:,i],hop));

    #Mixage
    canal_stereo_synth= np.column_stack((canal0_synth,canal1_synth))
    
    #Ecriture   
    wav.write('canal0_synth_src' + str(i) +'.wav',fs,canal_stereo_synth)

#plt.imshow(label)
#plt.show()










