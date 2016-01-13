clear, clc, close all
addpath('wavs/')
addpath('src/')
addpath('src/stft/')

% load a .wav file
[x, fs] = audioread('wavs/gauche.wav');     % get the samples of the .wav file
% x = x(:, 1);                        % get the first channel
% xmax = max(abs(x));                 % find the maximum abs value
% x = x/xmax;                         % scalling the signal

% define analysis parameters
xlen = length(x);                   % length of the signal
wlen = 1024;                        % window length (recomended to be power of 2)
h = wlen/4;                         % hop size (recomended to be power of 2)
nfft = 1024;                        % number of fft points (recomended to be power of 2)

% define the coherent amplification of the window
K = sum(hamming(wlen, 'periodic'))/wlen;

% perform STFT
[L, f, t] = stft(x(:,1), wlen, h, nfft, fs);
[R, ~, ~] = stft(x(:,2), wlen, h, nfft, fs);

% from interaural spectrogram extract phi(w,t) and alpha(w,t)
X_is = L./R;
phi_wt = angle(X_is);
alpha_wt = 20*log10(abs(X_is));
