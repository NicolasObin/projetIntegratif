import numpy as np, scipy

# x is a vector of data
# fs is the sample frequency
# T is the size of the window in seconds
# hop is the size of the hop in millisecondes
def stft(x, fs, T, hop):
    framesamp = int(T*fs)
    hopsamp = int(hop*fs)
    w = scipy.hanning(framesamp)
    X = scipy.array([scipy.fft(w*x[i:i+framesamp]) 
                     for i in range(0, len(x)-framesamp, hopsamp)])
    return X

# x is a vector of data
# fs is the sample frequency
# T is the size of the window in seconds
# hop is the size of the hop in millisecondes
def istft(X, fs, T, hop):
    x = scipy.zeros(T*fs)
    framesamp = X.shape[1]
    hopsamp = int(hop*fs)
    for n,i in enumerate(range(0, len(x)-framesamp, hopsamp)):
        x[i:i+framesamp] += scipy.real(scipy.ifft(X[n]))
    return x

