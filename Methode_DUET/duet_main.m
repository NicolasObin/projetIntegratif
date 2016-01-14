%DUET
clear all
close all

%% PARAMETRES %%
N = 1024;
M = 512;

%% Chargement des données %%
%aud='1.wav'
aud='4.wav'
[audio_time_data, fs]=audioread(aud);

[stft_data_chan1,stft_time_range,stft_freq_range] = stft(audio_time_data(:,1),N,M,fs);
[stft_data_chan2,~,~] = stft(audio_time_data(:,2),N,M,fs);

%Translation et on enleve la composante continue
stft_data_chan1=stft_data_chan1(2:end,:)';
stft_data_chan2=stft_data_chan2(2:end,:)';

%Affichage du spectrogramme du canal 1
% figure(1)
% imagesc(abs(stft_data_chan1'))
% ylab= linspace(0,stft_freq_range(end),11)';
% xlab= linspace(0,stft_time_range(end),11)';
% set(gca, 'YTickLabel', ylab(2:1:end))
% set(gca, 'XTickLabel', xlab(2:1:end))


%Construction de la matrice inter-aurale + eps pour eviter la div par 0
R=(stft_data_chan2+eps)./(stft_data_chan1+eps);

%Affichage du spectrogramme de la matrice inter_aurale
figure(2)
imagesc(abs(R))

%Construction du delta
freq=[(1:N/2) ((-N/2)+1:-1)]*(2*pi/(N)); %frequence sous forme de pulsation
lw0=repmat(freq,[size(R,1) 1]);
%Calcul des 0
zero_data=(stft_data_chan1~=0).*(stft_data_chan2~=0);
%delta
delta=angle(R)./lw0;
%Correction des 0
%delta(zero_data)=0;

%Construction du alpha
a=abs(R);
%Correction des 0
%a(zero_data)=1;
%alpha
alpha=(a-(1./a));

%Affichage
%figure(3)
%imagesc(sigma)
%figure(4)
%imagesc(alpha)

%%Construction de l'histogramme.
%   Build a 2-d histogram (one dimension is phase, one is amplitude) where 
%   the height at any phase/amplitude is the count of time-frequency bins that
%   have approximately that phase/amplitude.

p=1; q=0; %powers used to weight histogram
tfweight=(abs(stft_data_chan1).*abs(stft_data_chan2)).^p.*abs(lw0).^q; %weights vector

%histogram boundaries for alpha, delta
maxa=1;
maxd=4;

%number of hist bins for alpha, delta
abins=50;
dbins=100;

%only consider time-freq points yielding estimates in bounds
amask=(abs(alpha)<maxa)&(abs(delta)<maxd);
alphavec=alpha(amask);
deltavec=delta(amask);
tfweight=tfweight(amask);

%determine histogram indices (sampled indices?)
alphaind=round(1+(abins-1)*(alphavec+maxa)/(2*maxa));
deltaind=round(1+(dbins-1)*(deltavec+maxd)/(2*maxd));

%FULL-SPARSE TRICK TO CREATE 2D WEIGHTED HISTOGRAM
%A(alphaind(k),deltaind(k)) = tfweight(k), S is abins-by-dbins
H=full(sparse(alphaind,deltaind,tfweight,abins,dbins));

f=ones(4,4)*(1/16);

Hf = imfilter(H, f, 'replicate');

%plot2-Dhistogram
figure(3)
mesh(linspace(-maxd,maxd,dbins),linspace(-maxa,maxa,abins),Hf);

figure(4)
bar3(Hf)


%% Detection des sources
%Detection des pics définit comme étant 3/4 du max
pic=Hf>max(Hf(:))*3/4;

%labelisation
L = bwlabel(pic)

figure(5)
imagesc(L)

%Nombre de source
numsources=max(L(:));

for i=1:1:numsources
    %row=alpha
    %column=delta
    [r, c] = find(L==i)
    max_ind_alpha=round(mean(r(:)));
    max_ind_delta=round(mean(c(:)));
    %Stockage des centres
    peak_alpha(i,1)=maxa-(abins-max_ind_alpha)*(maxa*2/abins);
    peak_delta(i,1)=maxd-(dbins-max_ind_delta)*(maxd*2/dbins);
    %Stockage des puissances
    peak_alpha(i,2)=Hf(max_ind_alpha,max_ind_delta);
    peak_delta(i,2)=Hf(max_ind_alpha,max_ind_delta);
end

%Rangement par ordre de puissance
peak_alpha=sortrows(peak_alpha,2);
peak_delta=sortrows(peak_delta,2);

%nettoyage de la puissance
peak_alpha=peak_alpha(:,1);
peak_delta=peak_delta(:,1);

%convert alpha to a
peaka=(peak_alpha+sqrt(peak_alpha.^2+4))/2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%5.determine masks for separation
%6) Assign each time-frequency frame to the nearest peak in phase/amplitude 
%  space. This partitions the spectrogram into sources (one peak per source)

bestsofar=Inf*ones(size(stft_data_chan1));
bestind=zeros(size(stft_data_chan1));
for i=1:length(peak_alpha)
    score=abs(peaka(i)*exp(-sqrt(-1)*lw0*peak_delta(i)).*stft_data_chan1-stft_data_chan2).^2/(1+peaka(i)^2);
    mask=(score<bestsofar);
    bestind(mask)=i;
    bestsofar(mask)=score(mask);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%6.&7.demix with ML alignment and convert to time domain
%7) Then you create a binary mask (1 for each time-frequency point belonging to my source, 0 for all other points)
%8) Mask the spectrogram with the mask created in step 7.
%9) Rebuild the original wave file from 8.
%10) Listen to the result.
est=zeros(numsources,length(audio_time_data(:,1)));%demixtures

for i=1:numsources
    mask=(bestind==i);
    fft_synth=[zeros(1,size(stft_data_chan1,1))' ((stft_data_chan1+peaka(i)*exp(sqrt(-1)*lw0*peak_delta(i)).*stft_data_chan2)./(1+peaka(i)^2)).*mask];
    fft_synth=fft_synth(:,1:513)';
    esti=istft(fft_synth,M,N,fs);
    est(i,:)=esti(1:length(audio_time_data(:,1)))';
    
    %add back into the demix a little bit of the mixture
    %as that eliminates most of the masking artifacts
    soundsc(est(i,:),fs);% original code seems to have missed the transpose play demixture
    pause
end

