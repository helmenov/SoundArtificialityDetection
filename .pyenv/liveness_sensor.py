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

def liveness_sensor(fname, window_size=1024, frame_size=8192, shift=128):
    # load 2ch-wav file
    x, fs = sf.read(fname)
    len_x = x.shape[0]
    num_ch = x.shape[1]

    # define frame window
    window = (np.hanning(window_size + 1))[:window_size].reshape([window_size,1]) * np.ones([1,num_ch])

    # short-term fft
    i_start = 0
    n_frame = int(np.floor(len_x/shift))
    #n_frame = int(np.ceil(len_x/window_size))
    #IPR = np.zeros([int(frame_size/2),n_frame])
    #IGDD = np.zeros([int(frame_size/2-1),n_frame])
    #ICCR = np.zeros([int(frame_size),n_frame],dtype=np.complex)
    #ICCC = np.zeros([int(frame_size),n_frame],dtype=np.complex)
    #diffX = np.zeros([int(frame_size/2),n_frame-1],dtype=np.complex)
    Cep_past = np.zeros([int(frame_size),1])
    #Cep = np.zeros([int(frame_size),1],dtype=np.complex)
    CrossCep = np.zeros([n_frame-1])
    eps = 0.001
    minPow = 1
    while i_start + window_size - 1 < len_x - 1:
        x_now = np.zeros([frame_size,x.shape[1]])
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now[0:int(i_end-i_start),:] = window * x[int(i_start):int(i_end),:]
        # Length FFT target should be > window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)
        
        # Inter-channel Power Ratio
        Pow = np.real(X * np.conj(X))
        #IPR[0:int(frame_size/2),i_frame] = (Pow[0:int(frame_size/2),1]+eps) / (Pow[0:int(frame_size/2),0]+eps)
        
        # Inter-channel Group-delay Difference (kuroda)
        #Phase = np.unwrap(np.angle(X),np.pi)
        #f = np.array([range(0,int(frame_size/2))]).reshape([int(frame_size/2),1]) / window_size * fs
        #df = np.diff(f.reshape([1,int(frame_size/2)])).reshape([int(frame_size/2)-1,1])
        #dP_L = np.diff(Phase[0:int(frame_size/2),0].reshape([1,int(frame_size/2)])).reshape([int(frame_size/2)-1,1])
        #dP_R = np.diff(Phase[0:int(frame_size/2),1].reshape([1,int(frame_size/2)])).reshape([int(frame_size/2)-1,1])
        #G_L = dP_L/df
        #G_R = dP_R/df
        #IGDD[:,i_frame:i_frame+1] = G_R-G_L
        
        # Inter-frame diff-quefrency pass filter for L 
        quef = frame_size/4# zankyo jikan 0.9s == 0.9*window_size
        Amp = np.abs(X[:,0])
        #Phs = np.unwrap(np.angle(X[:,0])*2)/2
        #LS = np.zeros([int(frame_size),1],dtype=np.complex)
        #for i in range(0,int(frame_size)):
        #    LS[i] = complex(np.log(Amp[i]+eps), Phs[i])
        #Cep = scifft.ifft(LS) # complex cepstrum
        CepA = np.real(scifft.ifft(np.log(Amp+eps)))
        # minimum phase : echo cancelled 
        #Cep_min = np.r_[1,2*np.ones(int(frame_size/2-1)),np.ones(1-frame_size%2),np.zeros(int(frame_size/2-1))]
        #Cep_min = Cep_min * CepA
        # source : higher quef, filter : lower quef
        Lifter = np.r_[np.ones(int(quef)),np.zeros(int(frame_size-2*quef)),np.ones(int(quef))]
        #Cep_H = Cep * Cep_min
        Cep_H = Lifter * CepA
        Cep_H_mean = np.mean(Cep_H)
        Cep_H = Cep_H - Cep_H_mean
        if Pow[0,0] < minPow:
            minPow = Pow[0,0]
            min_frame = i_frame
            ref_Cep = Cep_H
                    
        if i_frame > 0:
            #diffCep = (Cep_H - Cep_past)/2
            #diffLS = scifft.fft(diffCep)
            #diffXall = np.exp(diffLS)
            #diffX[:,i_frame-1] = diffXall[0:int(frame_size/2)] 
            XCep = np.correlate(Cep_H[0:int(frame_size/2)], Cep_past[0:int(frame_size/2)],"full")
            ACep = np.correlate(Cep_H[0:int(frame_size/2)], Cep_H[0:int(frame_size/2)],"full")
            ACep_past = np.correlate(Cep_past[0:int(frame_size/2)], Cep_past[0:int(frame_size/2)],"full")
            XCep = XCep/np.sqrt(ACep * ACep_past)
            #print(XCep.shape)
            #CrossCep[i_frame-1] = np.nanmax(XCep)
            CrossCep[i_frame-1] = XCep[int(frame_size/2)]
            
        Cep_past = Cep_H
                
        i_start = i_start + shift

    CrossCep_ref = np.zeros([n_frame])
    i_start = 0
    while i_start + window_size - 1 < len_x - 1:
        x_now = np.zeros([frame_size,x.shape[1]])
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now[0:int(i_end-i_start),:] = window * x[int(i_start):int(i_end),:]
        # Length FFT target should be window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)
                
        # Inter-frame diff-quefrency pass filter for L 
        quef = window_size/4# zankyo jikan 0.9s == 0.9*window_size
        Amp = np.abs(X[:,0])
        #Phs = np.unwrap(np.angle(X[:,0])*2)/2
        #LS = np.zeros([int(frame_size),1],dtype=np.complex)
        #for i in range(0,int(frame_size)):
        #    LS[i] = complex(np.log(Amp[i]+eps), Phs[i])
        #Cep = scifft.ifft(LS) # complex cepstrum
        CepA = np.real(scifft.ifft(np.log(Amp+eps)))
        # minimum phase : echo cancelled 
        #Cep_min = np.r_[1,2*np.ones(int(frame_size/2-1)),np.ones(1-frame_size%2),np.zeros(int(frame_size/2-1))]
        #Cep_min = Cep_min * CepA
        # source : higher quef, filter : lower quef
        Lifter = np.r_[np.ones(int(quef)),np.zeros(int(frame_size-2*quef)),np.ones(int(quef))]
        #Cep_H = Cep[:,0] - Lifter * Cep_min
        Cep_H = Lifter * CepA
        Cep_H_mean = np.mean(Cep_H) 
        Cep_H = Cep_H - Cep_H_mean
            
        XCep = np.correlate(Cep_H[0:int(frame_size/2)], ref_Cep[0:int(frame_size/2)],"full")
        ACep = np.correlate(Cep_H[0:int(frame_size/2)], Cep_H[0:int(frame_size/2)],"full")
        ACep_ref = np.correlate(ref_Cep[0:int(frame_size/2)], ref_Cep[0:int(frame_size/2)],"full")
        XCep = XCep/np.sqrt(ACep * ACep_ref)
        #print(np.nanmax(XCep))
        #CrossCep_ref[i_frame] = np.nanmax(XCep) 
        CrossCep_ref[i_frame] = XCep[int(frame_size/2)] 
        i_start = i_start + shift
    
    
    return (CrossCep,CrossCep_ref,ref_Cep)
    
        
