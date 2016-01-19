# coding: utf8
import scipy, numpy as np
import scipy.io.wavfile as wav
import scipy.ndimage
import EAALib as eaa
import matplotlib.pyplot as plt


#%% PARAMETRES %%
N = 1024;  #Taille de fenetre
hop = 512; #Taille du saut

##Paramètre de l'histogramme
#Pondération (Par défaut)
p=1
q=0

#Limites pour alpha, delta dans l'histogramm
maxa=1;
maxd=4;

#Nombre de bin pour alpha et delta
abins=50;
dbins=100;


### Code DUET
## Preparation de l'audio
#Signal stereo
fs, data = wav.read('1.wav')

#Séparation des canaux
canal0=data[:,0]
canal1=data[:,1]

#Construction de la matrice temps-fréquence
c0_stft=eaa.stft(canal0,N,hop)
c1_stft=eaa.stft(canal1,N,hop)

#Suppression de la composante continue
#c0_con=c0_stft[:,0]
#c1_con=c1_stft[:,0]
c0_stft=scipy.delete(c0_stft,0,1)
c1_stft=scipy.delete(c1_stft,0,1)

##Histogramme
#Calcul de la matrice inter-aurale
R=eaa.matia(c0_stft,c1_stft)

#Calcul du alpha, du delta et de la matrice de frequence
alpha, delta, lw0 = eaa.alphadelta(R,N)

#Calcul de l'histogramme
H=eaa.histDuet(c0_stft,c1_stft,alpha,delta,lw0,p,q,maxa,maxd,abins,dbins)

#Filtrage
filt=np.ones((4,4))*(1/16)
Hf=scipy.ndimage.filters.correlate(H,filt)

## Detection des sources
#Detection des pics définits comme étant 2/4 du max
pic=Hf>np.max(Hf)*2/4;

#Labelisation
label, numsources =scipy.ndimage.measurements.label(pic)

#Initialisation du Tableau des pics
peak_alpha=np.zeros((numsources,1))
peak_delta=np.zeros((numsources,1))
#Remplissage du tableau des pics
for i in range(0,numsources) :
    #row=alpha
    #column=delta
    [r, c] = np.where(label==i+1);
    max_ind_alpha=np.round(np.mean(r));
    max_ind_delta=np.round(np.mean(c));
    #Stockage des centres
    peak_alpha[i,0]=maxa-(abins-(max_ind_alpha+1))*(maxa*2/abins);
    peak_delta[i,0]=maxd-(dbins-(max_ind_delta+1))*(maxd*2/dbins);

#Convertion de alpha vers a
peaka=(peak_alpha+np.sqrt(4+peak_alpha**2))/2;

##Creation des masques
# Assigne chaque frame temps-frequence (frame du spectrogramme) au pic le plus proche dans l'espace des phase/amplitude
# On partitionne donc le spectrogramme en source

bestsofar=np.Inf*np.ones(c0_stft.shape);
bestind=np.zeros(c0_stft.shape);
for i in range(0,numsources) :
    score=np.abs(peaka[i]*np.exp(-1j*lw0*peak_delta[i])*c0_stft-c1_stft)**2/(1+peaka[i]**2);
    mask=(score<bestsofar);
    bestind[mask]=i;
    bestsofar[mask]=score[mask];

##Reconstitution des sources
# Then you create a binary mask (1 for each time-frequency point belonging to my source, 0 for all other points)
# Mask the spectrogram with the mask created in step 7.

c0_stft_synth_array=np.zeros((c0_stft.shape[0],N,numsources),dtype=np.complex_)
c1_stft_synth_array=np.zeros((c0_stft.shape[0],N,numsources),dtype=np.complex_)

init=1;
for i in range(0,numsources) :

    #Séparation des sources
    mask=(bestind==i);

    #Application des masques
    #Pas bianire
    #c0_stft_synth=((c0_stft+peaka[i]*np.exp(-1j*lw0*peak_delta[i])*c1_stft)/(1+peaka[i]**2))*mask;
    #c1_stft_synth=((c1_stft+peaka[i]*np.exp(-1j*lw0*peak_delta[i])*c1_stft)/(1+peaka[i]**2))*mask;
    #Binaire
    c0_stft_synth=c0_stft*mask
    c1_stft_synth=c1_stft*mask

    #Rajout de la omposante continue trouquée précédemment 
    zero_pad=np.zeros([c0_stft.shape[0],1])
    c0_stft_synth=np.column_stack((zero_pad,c0_stft_synth))
    c1_stft_synth=np.column_stack((zero_pad,c1_stft_synth))

    #Stockage
    c0_stft_synth_array[:,:,i]=c0_stft_synth[:,:]
    c1_stft_synth_array[:,:,i]=c1_stft_synth[:,:]

#Génération des indices pour la puissance
ind_p=np.zeros((numsources,2))
ind_p[:,0]=np.arange(0,numsources,1)
for i in range(0,numsources) :
    ind_p[i,1]=np.sqrt(np.abs(np.sum(c0_stft_synth_array[:,:,i]**2)/c0_stft.shape[0]**2))
#print(ind_p)

#Tri des indices selon la puissance
ind_p= ind_p[np.argsort(ind_p[:,1])]
#print('--')
#print(ind_p)

#Tri du tableau de spectrogramme
c0_stft_synth_sorted_array=c0_stft_synth_array
c1_stft_synth_sorted_array=c0_stft_synth_array
for i in range(0,numsources) :
    c0_stft_synth_sorted_array[:,:,i]=c0_stft_synth_array[:,:,ind_p[i,0]]
    c1_stft_synth_sorted_array[:,:,i]=c1_stft_synth_array[:,:,ind_p[i,0]]

##Ecriture
for i in range(0,numsources) :    
    #Retour dans le domaine temporelle 
    canal0_synth=np.int16(eaa.istft(c0_stft_synth_sorted_array[:,:,i],hop));
    canal1_synth=np.int16(eaa.istft(c1_stft_synth_sorted_array[:,:,i],hop));

    #Mixage
    canal_stereo_synth= np.column_stack((canal0_synth,canal1_synth))
    
    #Ecriture   
    wav.write('canal0_synth_src' + str(i) +'.wav',fs,canal_stereo_synth)
    











