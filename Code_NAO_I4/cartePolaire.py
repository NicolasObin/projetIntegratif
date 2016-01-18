import matplotlib.pyplot as plt
import numpy as np


def cartePol(theta):
    #Creation du cercle
    plt.subplot(1, 1, 1, projection='polar')
    #theta=y, 2:x, 3:???, 4:taille de la fleche , alpha:intensite 
    #tracer la fleche
    plt.arrow(theta, 0, 0, 0.5, alpha =1, width = 0.017,edgecolor = 'blue')
    #colorer la zone 
    plt.bar(theta-np.pi/12, 1, width=0.5, bottom=0.0,color='red',edgecolor = 'blue')
    #affichage
    plt.show()
cartePol(np.pi/4)
