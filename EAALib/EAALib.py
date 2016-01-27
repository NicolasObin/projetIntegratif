# coding: utf8
# Bibliothèque EAALib pour la localisation et la séparation de source audio
# Codée par :
# Jérémy Renaudin - renaudin_jeremy@hotmail.fr - Version 1.1

import scipy, numpy as np
import math

#Construction de l'histogramme DUER
# c0_stft et c1_stft => Matrice temps frequence (Spectrogramme) des canaus
# alpha et delta : Matrice d'atténuation et de retard
# lw0 : Matrice des fréquence (pulsation)
# p, q : Pondération de l'histogramme (p=1 et q = 0 par def)
# maxa, maxd : limites de l'histogramme
# abins, dbins : Nombre de bins max de l'histogramme
def histDuet(c0_stft,c1_stft,alpha,delta,lw0,p,q,maxa,maxd,abins,dbins):
    #Tableau des poids
    tfweight=((abs(c0_stft)*abs(c1_stft))**p)*(abs(lw0)**q);

    #Constrution des masques
    amask=(abs(alpha)<maxa)&(abs(delta)<maxd);
    alphavec=alpha[amask];
    deltavec=delta[amask];
    tfweight=tfweight[amask];

    #Construction des indices de l'histogramme
    alphaind=np.round((abins-1)*(alphavec+maxa)/(2*maxa));
    deltaind=np.round((dbins-1)*(deltavec+maxd)/(2*maxd));

    #Construction de l'histogramme
    H=scipy.sparse.csc_matrix((tfweight,(alphaind,deltaind)),shape=(abins,dbins))
    #Sparse matrice ->Full Matrice
    H=H.todense()

    return H


#Calcul de l'alpha et du delta à partir de la matrice inter-aural pour la méthode DUET
#R matrice inter-aural
#N nombre de point de la stft
def alphadelta(R,N):
    #Construction du delta
    #Construction des matrices de frequence
    freq=np.concatenate((np.arange(1, N/2+1, 1),np.arange((-N/2)+1, 0, 1)),axis=0)*(2*np.pi/(N))
    lw0=np.tile(freq,(np.size(R,0),1));

    #Delta
    delta=-np.angle(R)/lw0;
    
    #Construction de l'alpha
    a=abs(R);

    #Alpha
    alpha=(a-(1/a));

    return alpha,delta,lw0

#Calcul de la matrice inter-aural
#Prend en argument deux matrice temporelle-fréquentielle (Spectrogramme)
def matia(stft1, stft2):

    #On rajoute eps pour eviter une division par 0
    eps=np.spacing(1)

    #Calcul de la matrice inter-aurale
    R=(stft2+eps)/(stft1+eps)
    return R


# x is a vector of data
# N is the size of the window frame
# hop is the size of the hop in frame
def stft(x, N, hop):
    framesamp = int(N)
    hopsamp = int(hop)
    w = scipy.hanning(framesamp)
    X = scipy.array([scipy.fft(w*x[i:i+framesamp]) 
                     for i in range(0, len(x)-framesamp, hopsamp)])
    return X

# x is a vector of data
# N is the size of the window frame
# hop is the size of the hop in millisecondes
def istft(X, hop):
    x = scipy.zeros((np.round(X.shape[1]/(X.shape[1]/hop)))*X.shape[0])
    framesamp = X.shape[1]
    hopsamp = int(hop)
    for n,i in enumerate(range(0, len(x)-framesamp, hopsamp)):
        x[i:i+framesamp] += scipy.real(scipy.ifft(X[n]))
    return x
	

#Calcul l angle pour des fréquences inférieur à  un kHz
#Prend en entrée deux vecteur de données de deux canaux issue d'une fft ou d'une frame de stft,
#ainsi que fs la frequence d echantillonage, c la vitesse du son dans l'air et d la distance entre les capteurs
#Retour un vecteur trié contenant la puissance et les angle pour chaque frequence (par odre croissant de puissance).
def compute_angle(canal1, canal2 , fs ,c, d):

    #Definition de la frequence max d'analyse pour le calcul de l'angle par difference de phase
    f_max=1000
    	
    #Calcul des bins d'interet
    bin_max= int(round(len(canal1)/(fs/f_max)))
    vect_bin = np.arange(0,bin_max,1)
    
    #Calcul des fréquences des bins
    f= np.arange(0,f_max,(f_max/float(bin_max)))
    
    #Correction pour éviter une division par 0
    f[0]=0.0001

    #On calcul la phase sur les bins d'interet
    phase_canal1 = np.angle(canal1[vect_bin]) 
    phase_canal2 = np.angle(canal2[vect_bin]) 

    #Calcul la puissance
    power=abs(canal1[vect_bin])+abs(canal2[vect_bin])

    #On calcul la difference de phase
    d_phase = phase_canal1 - phase_canal2

    #Resultat Round pour eviter les warning du à l'imprecision des float
    cos_angle=np.around(((c*d_phase)/(2*pi*f*d)), decimals=2)
    angle = np.real(np.lib.scimath.arccos(cos_angle)*180/np.pi)

    #Correction des résultats pour une fréquence de 0
    f[0]=0
    angle[0]=np.nan

    #Mise en forme des résultats
    stack_data=np.column_stack((power,angle,f))
    sort_stack_data= stack_data[np.argsort(stack_data[:,0])]

    return sort_stack_data

#Separation Duet
def compDuet(canal0,canal1,N,hop,p,q,maxa,maxd,abins,dbins,rejet_max_pic,rejet_max_score):

    #Construction de la matrice temps-fréquence
    c0_stft=stft(canal0,N,hop)
    c1_stft=stft(canal1,N,hop)

    #Suppression de la composante continue
    c0_stft=scipy.delete(c0_stft,0,1)
    c1_stft=scipy.delete(c1_stft,0,1)

    ##Histogramme
    #Calcul de la matrice inter-aurale
    R=matia(c0_stft,c1_stft)

    #Calcul du alpha, du delta et de la matrice de frequence
    alpha, delta, lw0 = alphadelta(R,N)

    #Calcul de l'histogramme
    H=histDuet(c0_stft,c1_stft,alpha,delta,lw0,p,q,maxa,maxd,abins,dbins)

    #Filtrage
    filt=np.ones((4,4))*(1./16)
    Hf=scipy.ndimage.filters.correlate(H,filt)

    ## Detection des sources
    pic=Hf>np.max(Hf)*rejet_max_pic;

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

    score=np.zeros((c0_stft.shape[0],c0_stft.shape[1],numsources));
    bestind=np.zeros((c0_stft.shape[0],c0_stft.shape[1],numsources));
    for i in range(0,numsources) :
        score[:,:,i]=np.abs(peaka[i]*np.exp(-1j*lw0*peak_delta[i])*c0_stft-c1_stft)**2/(1+peaka[i]**2);

    max_score=score.max(axis=2)

    for i in range(0,numsources) :
        bestind[:,:,i]=(score[:,:,i]>(np.max(score[:,:,i])*rejet_max_score))*(score[:,:,i]==max_score)


    ##Reconstitution des sources
    # Then you create a binary mask (1 for each time-frequency point belonging to my source, 0 for all other points)
    # Mask the spectrogram with the mask created in step 7.

    c0_stft_synth_array=np.zeros((c0_stft.shape[0],N,numsources),dtype=np.complex_)
    c1_stft_synth_array=np.zeros((c0_stft.shape[0],N,numsources),dtype=np.complex_)

    init=1;
    for i in range(0,numsources) :

        #Séparation des sources
        mask=bestind[:,:,i];

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

    #Tri des indices selon la puissance
    ind_p= ind_p[np.argsort(ind_p[:,1])]

    #Tri du tableau de spectrogramme
    c0_stft_synth_sorted_array=c0_stft_synth_array
    c1_stft_synth_sorted_array=c0_stft_synth_array
    for i in range(0,numsources) :
        c0_stft_synth_sorted_array[:,:,i]=c0_stft_synth_array[:,:,ind_p[i,0]]
        c1_stft_synth_sorted_array[:,:,i]=c1_stft_synth_array[:,:,ind_p[i,0]]

    return c0_stft_synth_sorted_array, c1_stft_synth_sorted_array, numsources
        
