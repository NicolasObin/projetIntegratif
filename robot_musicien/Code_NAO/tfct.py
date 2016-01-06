#!/usr/bin/env python

import scipy
import scipy.io as sio
from scipy.io import wavfile
import numpy as np
from oct2py import octave
from utility import *



def stft2(x, fftsize, overlap):   
    hop = fftsize / overlap
    w = scipy.hanning(fftsize+1)[:-1]      # better reconstruction with this trick +1)[:-1]  
    return np.array([np.fft.rfft(w*x[i:i+fftsize]) for i in range(0, len(x)-fftsize, hop)])

def istft2(X, overlap):   
    fftsize=(X.shape[1]-1)*2
    hop = fftsize / overlap
    w = scipy.hanning(fftsize+1)[:-1]
    x = scipy.zeros(X.shape[0]*hop)
    wsum = scipy.zeros(X.shape[0]*hop) 
    for n,i in enumerate(range(0, len(x)-fftsize, hop)): 
        x[i:i+fftsize] += scipy.real(np.fft.irfft(X[n])) * w   # overlap-add
        wsum[i:i+fftsize] += w ** 2.
    pos = wsum != 0
    x[pos] /= wsum[pos]
    return x

#if __name__ == '__main__':
def filtrage(input_name, output_name):
    # Create test signal and STFT.
	fs, data = wavfile.read(input_name)
	sig_py = pcm2float(data, 'float64')


    # Si on a plusieurs cannaux, on ne prends qu'une
	# tmp=np.shape(sig_oct)
    	# if (tmp[1]>1):
        #  	sig_oct=sig_oct[:,1]

	key_max = sio.loadmat('NAO_gris/A_key_left')
	key_max=key_max['A_key_left']

	wlen=1024
    	h=wlen/4
    	nfft=1024
	
	S_in = octave.hristo_stft(sig_py, wlen, h, nfft, fs)
	
	# S_in = stft2(sig_py, nfft, 4)

	tmp=np.shape(S_in)
	N_in=tmp[1]

	A_in = abs(S_in) # spectre d'amplitude

	[I,J]=np.shape(A_in)
	
	#P_in=np.zeros(np.shape(A_in))	
	P_in = octave.angle(S_in) # spectre de phase

	A_out=np.zeros(np.shape(A_in))	

	for i in range(0,N_in-1):
		# A_out[i,:]=((A_in[i,:]-key_max.T))

        	A_out[:,i]=(A_in[:,i]-key_max.T)


    	P_out = P_in
	A_out_seuille=np.zeros(np.shape(A_in))
    
	for i in range(1,I):
        	for j in range(1,J):
            		if A_out[i,j]>0:
                		A_out_seuille[i,j]=A_out[i,j]


	# on reconstruit le spectre complexe
	S_out = A_out_seuille*np.exp(1j*P_out)

    	output = octave.hristo_istft(S_out, h, nfft, fs)
	# output = istft2(S_out, 4)

	wavfile.write(output_name, fs, float2pcm(output.T, 'int16'))
