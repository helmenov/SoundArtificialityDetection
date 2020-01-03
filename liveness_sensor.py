# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""
import soundfile as sf
import scipy.fftpack as scifft
import numpy as np
import matplotlib.pyplot as plt

def Power_Spectrum(x, window_size=1024, is_input_spectrum=0, is_input_windowed=0):
    len_x = x_shape[0]
    num_ch = x_shape[1]
    
    if is_input_windowed:
        window = (np.hanning(window_size + 1))[:window_size].reshape([window_size,1]) * np.ones([1,num_ch])
        x_w = window * x
    else:
        x_w = x
        
    if is_input_spectrum:
        spec = np.fft(x_w)
    else:
        spec = x
    
    pspec = spec[0:int(window_size/2)] * np.conj(spec[0:int(window_size/2)])
    return pspec

def Group_Delay(x, window_size=1024, fs=44100, is_input_spectrum=0, is_input_windowed=0):
    len_x = x_shape[0]
    num_ch = x_shape[1]
    
    if is_input_windowed:
        window = (np.hanning(window_size + 1))[:window_size].reshape([window_size,1]) * np.ones([1,num_ch])
        x_w = window * x
    else:
        x_w = x
        
    if is_input_spectrum:
        spec = np.fft(x_w)
    else:
        spec = x
        
    f = np.array([range(0,int(window_size/2))]).reshape([int(window_size/2),1]) / window_size * fs
    df = np.diff(f.reshape([1,int(window_size/2)])).reshape([int(window_size/2)-1,1])
    Phs = np.unwrap(np.angle(spec[0:int(window_size/2)]))
    dPhs = np.diff(Phs[0:int(window_size/2),0].reshape([1,int(window_size/2)])).reshape([int(window_size/2)-1,1])
    gd = dPhs/df
    return gd

def Complex_Cepstrum(X, window_size=1024, is_input_spectrum=0, is_input_windowed=0):
    len_x = x_shape[0]
    num_ch = x_shape[1]
    
    if is_input_windowed:
        window = (np.hanning(window_size + 1))[:window_size].reshape([window_size,1]) * np.ones([1,num_ch])
        x_w = window * x
    else:
        x_w = x
        
    if is_input_spectrum:
        spec = np.fft(x_w)
    else:
        spec = x
        
    amp = np.abs(spec)
    phs = np.unwrap(np.angle(spec))
    logspec = np.log(amp) + i*phs;
    ceps = np.fft(logspec);
    return ceps

def liveness_sensor(fname, window_size=1024):
    # load 2ch-wav file
    x, fs = sf.read(fname)
    len_x = x.shape[0]
    num_ch = x.shape[1]

    # define frame window
    window = (np.hanning(window_size + 1))[:window_size].reshape([window_size,1]) * np.ones([1,num_ch])
    shift = window_size/2

    # short-term fft
    i_start = 0
    n_frame = int(np.ceil(len_x/shift))
    #n_frame = int(np.ceil(len_x/window_size))
    IPR = np.zeros([int(window_size/2),n_frame])
    IGDD = np.zeros([int(window_size/2-1),n_frame])
    ICCR = np.zeros([int(window_size),n_frame],dtype=np.complex)
    ICCC = np.zeros([int(window_size),n_frame],dtype=np.complex)
    eps = 0.001
    while i_start + window_size - 1 < len_x - 1:
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now = window * x[int(i_start):int(i_end),:]
        # Length FFT target should be window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)
        
        # Inter-channel Power Ratio
        Pow = np.real(X * np.conj(X))
        IPR[0:int(window_size/2),i_frame] = (Pow[0:int(window_size/2),1]+eps) / (Pow[0:int(window_size/2),0]+eps)
        
        # Inter-channel Group-delay Difference
        Phase = np.unwrap(np.angle(X),np.pi)
        f = np.array([range(0,int(window_size/2))]).reshape([int(window_size/2),1]) / window_size * fs
        df = np.diff(f.reshape([1,int(window_size/2)])).reshape([int(window_size/2)-1,1])
        dP_L = np.diff(Phase[0:int(window_size/2),0].reshape([1,int(window_size/2)])).reshape([int(window_size/2)-1,1])
        dP_R = np.diff(Phase[0:int(window_size/2),1].reshape([1,int(window_size/2)])).reshape([int(window_size/2)-1,1])
        G_L = dP_L/df
        G_R = dP_R/df
        IGDD[:,i_frame:i_frame+1] = G_R-G_L
        
        # Inter-channel Ratio of Cepstrum
        # log spectrum: ln(M exp(i\theta)) = lnM + i\theta
        # complex cepstrum: C = fft(lnM+i\theta) , \theta:unwrapped
        # inter-channel: C_R/C_L
        Amp_L = np.abs(X[:,0]);
        Phs_L = np.unwrap(np.angle(X[:,0])*2)/2;
        LS_L = np.zeros([int(window_size),1],dtype=np.complex)
        for i in range(0,int(window_size)):
            LS_L[i] = complex(np.log(Amp_L[i]+eps), Phs_L[i]);
        C_L = scifft.fft(LS_L);
        Amp_R = np.abs(X[:,1]);
        Phs_R = np.unwrap(np.angle(X[:,1])*2)/2;
        LS_R = np.zeros([int(window_size),1],dtype=np.complex)
        for i in range(0,int(window_size)):
            LS_R[i] = complex(np.log(Amp_R[i]+eps), Phs_R[i]);
        C_R = scifft.fft(LS_R);
        ICCR[0:int(window_size),i_frame:i_frame+1] = (C_R+eps)/(C_L+eps) 
        #ICCR[0:int(window_size),i_frame:i_frame+1] = C_R[0:int(window_size)]
        
        # inter-channel correlation of Cepstrum
        C_R = C_R - C_R.mean()
        C_L = C_L - C_L.mean()
        ICCC[0:int(window_size),i_frame] = np.correlate(np.real(np.squeeze(C_R)),np.real(np.squeeze(C_L)),"same")
        
        i_start = i_start + shift;
    return (IPR,IGDD,ICCR,ICCC)
    
IPR, IGDD, ICCR, ICCC = liveness_sensor("60.wav",1024)
        
