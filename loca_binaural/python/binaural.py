# JM
# VIEUX TRUC, PREFERER LOCA_NAO.PY
import scipy, numpy as np
import scipy.io.wavfile as wav
import pylab

def binaural(fichierwav,dist):
	fs, my_audio = wav.read(fichierwav,'r')
	fft_audio = scipy.fft(my_audio)
	# pic de frequence pour chaque micro
	args = []
	vals = []
	for ii in np.arange(0,3):
		args = [args np.argmax(fft_audio[:,ii])]
		vals = [vals np.max(ftt_audio[:,ii])]
	print 'bin freq max pour chaque micro. on les espere identiques'
	print args
	# différence de phase pour chaque pic et chaque paire de micros
	#delta = []
	## on commence par travailler uniquement avec le picg
	#delta = [delta np.angle
		
		
	
