import os, sys
import subprocess
import pyoracle
from IPython.core.display import Image
from scipy.io import wavfile
import numpy as np

def runPyOracle(filename):
    
    [head, tail] = os.path.split(filename)
    
    fft_size = 8192	 #Taille de chaque fft (en echantillon)
    hop_size = fft_size/2 #"Hop" entre chaque fft (tjrs fft_size/2)
    featuretodo = 'chroma'
    features = pyoracle.make_features(filename, fft_size, hop_size, featuretodo)
    frames_per = 1
    
    threshold = (0, 1.5, 0.05)
    alpha = 1
    analysismode='cum'
    ideal_t = pyoracle.calculate_ideal_threshold(threshold, features, featuretodo, frames_per, alpha, analysismode, 'euclidian')

    oracle = pyoracle.make_oracle(ideal_t[0][1], features, featuretodo, frames_per)
    p = 0.6
    k = 0
    lrs = 5 	
    seq_len = 70
    
    outputFilename = head + os.sep + tail.strip('.wav') + '_impro.wav'
    
    a = pyoracle.Resources.generate.generate_audio(filename, outputFilename, fft_size, hop_size, oracle, seq_len, p, k, lrs)

    return [outputFilename,seq_len]

def runBeatTracking(filename):
    
    [head, tail] = os.path.split(filename)
    
    outputFilename = head + os.sep + tail.strip('.wav') + '_beat.wav'
    
    subprocess.call(["aubiotrack", "-i", filename, "-o", outputFilename, "-f"])
    output = subprocess.check_output(["aubioquiet", "-i", outputFilename])

    fileName = 'output.txt'
    
    file = open(fileName, 'w')
    file.write(output)
    file.close

    file = open(fileName, 'r')

    quietTime = 0
    noisyTime = 0
    beatTime = ()

    isFirstValue = True

    while True:
 
        line1 = file.readline()
        line1 = line1.strip('NOISY: ')
        
        if line1 == '':
            break

        noisyTime = float(line1)

        if isFirstValue:
            firstValue = noisyTime
            isFirstValue = False

        beatTime = beatTime + (noisyTime - quietTime,)
        
        line2 = file.readline()
        line2 = line2.strip('QUIET: ')
        quietTime = float(line2)
    
    
    #Compute the average
    meanBeat = np.mean(beatTime)

    return [meanBeat,firstValue]
