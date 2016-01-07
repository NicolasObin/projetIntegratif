% AEG MATLAB
% JM

% 06/01 ajout STFT, test sur fichiers du nao, avec debruitage
% 04-05/01 code initial


clear all

%% parametres
% TFCT
N = 512;
M = 0;
% AEG
% d = 0.32; % pour fichiers N Obin
d = 0.135; % pour fichiers Nao
c = 340;
fs = 44100;
% mode
% FFT_or_STFT = 'fft';
FFT_or_STFT = 'stft';


%% localisation

% load sine440_angle1.mat
% son = x_mic;

% canaux non debruites
% [son, fs] = audioread('droite_45.wav');
% droite = son(:,2);
% gauche = son(:,1);
% canaux debruites
[droite, ~] = audioread('face_debruiteCan2.wav');
[gauche, fs] = audioread('face_debruiteCan1.wav');

if strcmp(FFT_or_STFT,'fft') % avec FFT sur tout le signal
    disp('methode avec la FFT sur tout le signal')
    % calcul de la fft
    L = length(droite);
    f = fs*(0:(L/2))/L;
    X_droite = fft(droite);
    X_gauche = fft(gauche);
    % pic de la fft
    [val_d, ind_d] = max(abs(X_droite(100:end)));
    [val_g, ind_g] = max(abs(X_gauche(100:end)));
    % diff de phase
    delta = angle(X_droite(ind_d)) - angle(X_gauche(ind_g));
    % AEG
    theta_estime = acos((c*delta) / (2*pi*f(ind_d)*d));
    disp(['angle estime :' num2str(real(theta_estime*180/pi))])
    
elseif strcmp(FFT_or_STFT,'stft') % avec la STFT
    disp('methode avec la TFCT')
    [X_droite,~,~] = stft(droite,N,M,fs);
    [X_gauche,t,f] = stft(gauche,N,M,fs);
    
    angle_est = [];
    for timestep = 1:size(X_droite,2)
        [val,f_bin] = max(abs(X_droite(:,timestep)));
        if f_bin == 257
            f_bin = 256;
        end
        % diff de phase
        delta = angle(X_droite(f_bin,timestep)) - angle(X_gauche(f_bin,timestep) );
        % AEG
        (c*delta) / (2*pi*f(f_bin)*d)
        theta_estime = acosd((c*delta) / (2*pi*f(f_bin)*d));
        angle_est = [angle_est real(angle(theta_estime))];
        %debug
%         val
%         f_bin
%         angle(X_droite(f_bin,timestep))
%         angle(X_gauche(f_bin,timestep))
%         disp(['delta : ' num2str(delta)])
%         real(angle(theta_estime))
%         pause
    end
    bar(angle_est)
end
