% DENOISER DU PROJET "NAO MUSICIEN" de 2014-2015
% mis à jour/corrigé par JM (PROJET "ECOUTE ACTIVE" 2015-2016)
%
% le dossier data/ contient les signatures spectrales de bruit pour chaque
% micro. ces signatures spectrales sont celles de "NAO MUSICIEN"
% le script sauve le fichier debruité dans le même dossier que le fichier
% d'orgine, format wav

clear all; close all; clc;
addpath('src/')

% Fichier à débruiter
fichier = 'wavs/droite_45.wav';
[input, fs]=audioread(fichier);
% choix du canal
CHOIX = menu('Choisissez un micro','Left','Right','Front','Rear');
% denoise
output = NAO_denoiser( input, fs, CHOIX );
% ecriture du canal débruité
audiowrite(strcat(fichier(1:end-4),'_debruiteCan',num2str(CHOIX),'.wav'),output,fs);
