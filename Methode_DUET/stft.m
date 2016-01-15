%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%              Short-Time Fourier Transform            %
%               with MATLAB Implementation             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% data=> signal audio, fentre => string contenant le choix de la fentre, N=> Nombre de point FFT, M=> Nombre de point recouvrement, fs=>Fréquence d'échantillonnage). 
function [X,t,f] = stft(data,N,M,fs)

%Construction de l'axe des f
f=0:fs/N:fs-(fs/N);

%Construction de l'axe des t
t=[0:1:length(data)]*(1/fs);

iter=ceil(length(data)/(N-M));

%On bourre de 0 pour la dernière trame    
dataBourree=zeros(1,N*iter);
dataBourree([1:length(data)])=data;

X=[];
for i=1:1:iter
%Découpage d'un buffer
buffer=dataBourree([1+((i-1)*(N-(M))):1:((i-1)*(N-(M)))+N]);
%Application d'un fenetrage de Hanning
%OK
buffer=buffer'.*hamming(N, 'periodic');
K=fft(buffer);
X=[X K];
end


end