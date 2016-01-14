#!/usr/bin/env python

import scipy, pylab, time
import wave
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from oct2py import octave
from utility import *


if __name__ == '__main__':
	
	print 'Lecture'	
	[sig_oct,fs,nbit]=octave.wavread("wavs/test8.wav")

	micro=1 # 1=left, 2=right, 3=front, 4= rear, otherwise=error
	print 'Process'
	output = octave.NAO_denoiser( sig_oct, fs, micro )
	print 'Ecriture'
	wavfile.write('output4.wav', fs, float2pcm(output.T, 'int16'))
