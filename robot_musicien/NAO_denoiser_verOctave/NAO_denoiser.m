function [ output ] = NAO_denoiser( input, fs, micro )
% This function eliminates the noise recorded from the 4 microphones of
% NAO.
% function [ output ] = NAO_denoiser( wav_path, micro )
addpath('data/');
    switch micro
        case 1
            key_max=load ('A_key_left.mat');
            key_max=key_max.A_key_left;
        case 2
            key_max=load ('A_key_right.mat');
            key_max=key_max.A_key_right;
        case 3
            key_max=load ('A_key_front.mat');
            key_max=key_max.A_key_front;
        case 4
            key_max=load ('A_key_rear.mat');
            key_max=key_max.A_key_rear;
        otherwise
            error('I dont know why');
    end
    
    % Si on a plusieurs cannaux, on ne prends qu'une
    if (size(input,2)>1)
        input=input(:,micro);
    end
    
    wlen=1024;  % Taille de fenêtre de Hamming
    h=wlen/4;   % overlap;
    nfft=wlen;  % Nombre de point de Transformé de Fourrier

    [S_in] = hristo_stft(input, wlen, h, nfft, fs);

    %plot_spect(S_in);
    %title('Spectogramme Avant Traitement');
    %xlabel('Temps (s)');ylabel('Fréquence (Hz)');
    
    N_in=size(S_in,2);

    A_in = abs(S_in); % spectre d'amplitude
    P_in = angle(S_in); % spectre de phase

    A_out=zeros(size(A_in));

    for i = 1:N_in
        A_out(:,i)=A_in(:,i)-key_max;
    end

    P_out = P_in;

    [I,J]=size(A_out);
    A_out_seuille=zeros(I,J);
    
    for i=1:I
        for j=1:J
            if A_out(i,j)>0
                A_out_seuille(i,j)=A_out(i,j);
            end
        end
    end
    
    A_out=A_out_seuille;

    % on reconstruit le spectre complexe
    S_out = A_out_seuille.*exp(1j*P_out);

    %plot_spect(S_out);
    %title('Spectogramme Apres Traitement');
    %xlabel('Temps (s)');ylabel('Fréquence (Hz)');
    
    output = hristo_istft(S_out, h, nfft, fs);

end

