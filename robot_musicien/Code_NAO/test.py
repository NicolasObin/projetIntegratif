#coding: latin-1
import os, sys

import pyoracle
from IPython.core.display import Image
from scipy.io import wavfile
import numpy as np
from optparse import OptionParser

def improgeneration(filename):

	#filename = 'FunkBass.wav' #fichier d'entrée
	fft_size = 8192*2	 #Taille de chaque fft (en echantillon)
	hop_size = fft_size/2 #"Hop" entre chaque fft (tjrs fft_size/2)
	featuretodo = 'chroma' #string contenant les caractéristiques selon lesquelles on va construite l'oracle : doit concorder avec le vecteur features j'imagine ??
	#Si je comprend bien, on echantillone le son en entrée avec des ffts de taille indiquée ci-dessus, puis on zappe "hop_size" echantillons avant la prochaine
	features = pyoracle.make_features(filename, fft_size, hop_size, featuretodo) #Extrait les caractéristiques d'un morceau, choisies en dernier argument de la fonction, choix 
																			  #possibles : 'mfcc', 'rms', 'centroid', 'chroma', and/or 'zerocrossings'
																			  #rms : "root mean square", puissance "efficace" la puissance dispo tt le temps en regime etabli..?
																			  #mfcc : "mel frequency cepstrum", representation a court terme du spectre de puissance d'un son
																			  #centroid : mesure pour caracteriser un spectre, indique ou le "centre de masse" de celui-ci es	
																			  #chroma : representation ou le spectre entier est projeté sur 12 bits representarespectivement les 12 demitons distincs (ou chromacité) de l'oct																		  
																			  #zerocrossings : releve les endroits ou le signal change de signe (passe par 0																		  
																			  #Lesquelles choisir ???? Compromis pour avoir la meilleure impro possible mais aussi pas trop 
	
	frames_per = 1#Nombre moyen de sequences a analysé pour générer un état de l''oracle

	threshold = (0, 3, 0.05) #Range sur laquelle on va tester les seuils : de 0 à 1 par pas de 0.02
	alpha = 1
	analysismode='cum'
	ideal_t = pyoracle.calculate_ideal_threshold(threshold, features, featuretodo, frames_per, alpha, analysismode, 'euclidian')
	#Features : vecteur de caractéristiques calculé au dessus
	#alpha : utilisé pour garder le taux d'information > 0 (laisser à 1)
	#analysismode : la méthode d'estimation du taux d'information, 'cum' pour l'alphabet cumulatif (par défaut), 'old' pour la vieille méthode (mais pas expliqué...) -> test ?
	#distance :  distance utilisée pour la construction de l'oracle : peut etre 'euclidian' ou 'bregman' 

	#Calcule l'oracle avec les parametres calculés au dessus (meilleurs seuils : ideal_t)
	#features : vecteur de features calculé au dessus
	#featuretodo : pareil qu'au dessus.. 
	#frames_per_state : pareil aussi
	oracle = pyoracle.make_oracle(ideal_t[0][1], features, featuretodo, frames_per)
	# pyoracle.draw_oracle(best_oracle, 'boutput.png', size=(1200, 400))
	# Image(filename='boutput.png')
	pyoracle.draw_oracle(oracle, 'oracledraw.png', size=(1000,400))
	#Generation audio avec l'oracle calculé juste au dessus d'une impro de taille réglable
	#fft et hop : doivent etre les memes que ci dessus
	p = 0.75#Paramètre de continuité : probabilité de saut d'une séquence à l'autre : trouver le bon réglage (0.75?  si 1 on ne change rien, plus il est petit plus ca saute)
	k = 0 #Point de départ de l'analyse 
	lrs = 1 #Controle la quantité de contexte musical partagé qui doit etre partagé entre deux états avant un saut. Haute valeur -> transitions plus smooth quand on jump
			#mais limitera le nombre de sauts : -> compromis
	seq_len = 250 #longueur de la séquence à générer en frames (du coup nombre de fft)
	a = pyoracle.Resources.generate.generate_audio(filename, 'output1.wav', fft_size, hop_size, oracle, seq_len, p, k, lrs)
	# a = pyoracle.Resources.generate.generate_audio('prokofiev.wav', 'output2.wav', fft_size, hop_size, oracle, seq_len, p, k, lrs)
	# a = pyoracle.Resources.generate.generate_audio('prokofiev.wav', 'output3.wav', fft_size, hop_size, oracle, seq_len, p, k, lrs)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="Write input filename", metavar="FILE")
	(option,args)=parser.parse_args()
	improgeneration(option.filename)
	