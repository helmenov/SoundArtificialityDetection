# -*- coding: utf-8 -*-
#%%
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""
from numpy.lib.index_tricks import nd_grid
import soundfile as sf
import scipy.fftpack as scifft
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def rcunwrap(x):
    '''
        unwrap  the phase and removes phase corresponding to integer lag.
    '''
    n = len(x)
    nh = int(np.floor((n+1)/2))
    y = np.unwrap(x)
    nd = np.round((y[nh]/np.pi))
    for i in range(len(y)):
        y[i] = y[i] - np.pi*nd*i/nh
    return y, nd

def replay_sensor(fname, window_size=1024, frame_size=8192, shift=128):
    # load 2ch-wav file
    x, fs = sf.read(fname)
    len_x = len(x)
    num_ch = x.ndim
    x = x.reshape([len_x,num_ch])[:,0]
    x = np.squeeze(x)
    print(x.shape)

    # define frame window
    window = (np.hanning(window_size + 1))[:window_size]

    # short-term fft
    i_start = 0
    n_frame = int(np.floor(len_x/shift))

    peak_count = np.zeros([n_frame])
    eps = 1 #1e-20

    quef = window_size/64
    Cep_Hs = np.zeros([int(quef),n_frame])
    while i_start + window_size - 1 < len_x - 1:
        x_now = np.zeros([frame_size,])
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now[0:int(i_end-i_start)] = window * x[int(i_start):int(i_end)]
        # Length FFT target should be > window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)/frame_size
        X = scifft.fftshift(X) #**2021.01.26 kotaro**#
        
        Amp = np.sqrt(X * np.conj(X))
        #Phs = np.unwrap(np.angle(X))   # ** changed 2021.1.26 kotaro**
        Phs, nd = rcunwrap(np.angle(X))
        print(nd)
        Phs = Phs - Phs[int(frame_size/2)]  # ** added 2021.1.26 kotaro**
        LS = np.zeros([int(frame_size)],dtype=np.complex)
        for i in range(0,int(frame_size)):
            LS[i] = complex(np.log(Amp[i]+eps), Phs[i])
        Cep = scifft.ifft(LS) 

        Cep_complex = np.squeeze(Cep) # complex cepstrum　複素ケプストラム

        Cep_Amplitude = scifft.ifft(np.log(Amp+eps)) # amplitude cepstrum　振幅ケプストラム

        # minimum phase : echo cancelled source 最小位相ケプストラム．ピークは音源調音の基本周波数の逆数
        Cep_MinPhase = np.r_[1,2*np.ones(int(frame_size/2-1)),np.ones(1-frame_size%2),np.zeros(int(frame_size/2-1))]
        Cep_MinPhase = Cep_MinPhase * Cep_Amplitude # minimum phase cepstrum
        
        # allphass transfer function オールパスケプストラム．ピークは室内伝達関数の基本周波数の逆数
        Cep_Allpass = Cep_complex - Cep_MinPhase

        # source : higher quef, filter : lower quef　低ケプストラムに調音成分，高ケプストラムに駆動信号成分
        Lifter = np.r_[np.ones(int(quef)),np.zeros(int(frame_size-2*quef)),np.ones(int(quef))]
        
        #Cep_H = Lifter * Cep_MinPhase
        #Cep_H = Lifter * Cep_complex
        #Cep_H = Lifter * Cep_Amplitude
        Cep_H = Lifter * np.real(Cep_Allpass)
        
        Cep_Hs[0:int(quef),i_frame] = Cep_H[0:int(quef)]
        peak_count[i_frame] = len(signal.argrelmax(Cep_H[0:int(quef)],order=5)[0]) 

        if i_frame == 5:
            fig = plt.figure(figsize=(3,10),dpi=100,tight_layout=True) #####
            ax1 = fig.add_subplot(511)
            f = np.arange(-frame_size/2,frame_size/2)/fs/frame_size*1000
            ax1.plot(f,np.real(scifft.fftshift(Cep_complex)),'-')
            ax1.set_ylabel("Complex")
            ax1.set_xlabel('quefrency [ms]')
            ax2 = fig.add_subplot(512)
            ax2.plot(f,np.real(scifft.fftshift(Cep_Amplitude)),'-')
            ax2.set_ylabel("Amplitude")
            ax2.set_xlabel('quefrency [ms]')
            ax3 = fig.add_subplot(513)
            ax3.plot(f,np.real(scifft.fftshift(Cep_MinPhase)),'-')
            ax3.set_ylabel("Minimum Phase")
            ax3.set_xlabel('quefrency [ms]')
            ax4 = fig.add_subplot(514)
            ax4.plot(f,np.real(scifft.fftshift(Cep_Allpass)),'-')
            ax4.set_ylabel("Allpass")
            ax4.set_xlabel('quefrency [ms]')
            ax5 = fig.add_subplot(515)
            q = f[int(frame_size/2):]
            ax5.plot(q[:int(quef)],np.real(Cep_H[:int(quef)]),'-')
            ax5.set_xlabel('quefrency [ms]')

        i_start = i_start + shift

    return peak_count, Cep_Hs

WavHome = "Audacity3/"

window_size = 8192
frame_size = 8192
shift = int(window_size/2)


labelname = ["","","",""]
#wavname = ["0001.flac","5401.flac","5603.flac","5805.flac"]
#wavname = ["0011.flac","5422.flac","5624.flac","5826.flac"]
wavname = ["0051.wav","5502.flac","5704.flac","5906.flac"]
#wavname = ["PA_D_0000001.flac","PA_D_0005401.flac","PA_D_0005603.flac","PA_D_0005805.flac"]

#%%
wavname_path = WavHome+wavname[0]
x, fs = sf.read(wavname_path)
x = x.reshape([len(x),x.ndim])
x = x[:,0]

len_x = len(x)
quef = int(window_size/16)    
n_frame = int(np.floor(len_x/shift))
Cep_Hs = np.zeros([6,quef,n_frame])
ref_Cep = np.zeros([6,quef]) 
min_frame = np.zeros([6,])


peak_count, Cep_Hs = replay_sensor(wavname_path,window_size,frame_size,shift)


# %%
