% AEG MATLAB
% JM - derniere modif le 05/01

clear all

%% parametres
% TFCT
N = 512;
M = 0;
% AEG
d = 0.32;
f0 = 440;
c = 340;
fs = 44100;

% [son, fs] = audioread('audio_AEG.wav');
load sine440_angle1.mat
son = x_mic;

droite = son(:,1);
gauche = son(:,2);

% [X_droite,t,f] = stft(droite,N,M,fs);
% [X_gauche,t,f] = stft(gauche,N,M,fs);

X_droite = fft(droite);
X_gauche = fft(gauche);

[val_d, ind_d] = max(abs(X_droite));
[val_g, ind_g] = max(abs(X_gauche));

% diff de phase
delta = angle(X_droite(ind_d)) - angle(X_gauche(ind_g));
theta_estime = acos((c*delta) / (2*pi*f0*d));
real(theta_estime*180/pi)

% avec la STFT (non fonctionnel)
% angle_est = [];
% for timestep = 1:87;
%     delta = angle(X_droite(f_ind,timestep)) - angle(X_gauche(f_ind,timestep) );
%     %% Modele epipolaire
%     theta_estime = acosd((c*delta) / (2*pi*f(f_ind)*d));
%     angle_est = [angle_est real(angle(theta_estime))];
% end
% angle_est

