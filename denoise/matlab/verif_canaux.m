% Ce script a pour objectif de verifier quel micro correspond a quel canal
% du fichier wav
% 06/01 - JM
clear all, close all, clc
[son, Fs] = audioread('wavs/gauche.wav');

%% l'ordre de grattage est : right, front, left, rear

player = audioplayer(son(:,1), Fs);
play(player);

% canal 1 -> left
% canal 2 -> right
% canal 3 -> front
% canal 4 -> rear