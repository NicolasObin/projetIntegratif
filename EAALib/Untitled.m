data=wavread('1.wav');
can1=data(:,1);
can2=data(:,2);
crr=xcorr(can1,can2);
[a,c]=max(crr)

data2=wavread('canal0_synth_src2.wav');
can1=data2(:,1);
can2=data2(:,2);
crr=xcorr(can1,can2);
[a,c]=max(crr)

data1=wavread('canal0_synth_src1.wav');
can1=data1(:,1);
can2=data1(:,2);
crr=xcorr(can1,can2);
[a,c]=max(crr)