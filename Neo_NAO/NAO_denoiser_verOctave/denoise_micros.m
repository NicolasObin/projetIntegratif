clear all; close all; clc;

CHOIX=2;%menu('Choisissez une micro','Left','Right','Front','Rear');

addpath('wavs/');

[input, fs, nbits]=wavread('Etienne.wav');

output = NAO_denoiser( input, fs, nbits, CHOIX );

wavwrite(output,fs, nbits, 'x_denoised');

%figure;
%plot(input(:,CHOIX));
%hold on;
%plot(output,'y');
%title('Signal Temporaire');
%xlabel('Temps (s)');ylabel('Amplitude (V)');
%legend('Avant','Après');
