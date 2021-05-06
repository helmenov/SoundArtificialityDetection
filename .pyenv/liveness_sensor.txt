# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""
import soundfile as sf
import scipy.fftpack as scifft
import numpy as np
import scipy.signal as signal

def liveness_sensor(fname, window_size=1024, frame_size=8192, shift=128):
    # load 2ch-wav file
    x, fs = sf.read(fname)
    len_x = len(x)
    num_ch = x.ndim
    x = x.reshape([len_x,num_ch])

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
    peak_count = np.zeros([n_frame])
    eps = 1e-10
    wd = 1
    refPow = frame_size
    quef = window_size/16
    Cep_Hs = np.zeros([int(quef),n_frame])
    while i_start + window_size - 1 < len_x - 1:
        x_now = np.zeros([frame_size,x.ndim])
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now[0:int(i_end-i_start),:] = window * x[int(i_start):int(i_end),:]
        # Length FFT target should be > window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)/frame_size
        
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
        Amp = np.abs(X[:,0])
        Phs = np.unwrap(np.angle(X[:,0])*2)/2
        LS = np.zeros([int(frame_size),1],dtype=np.complex)
        for i in range(0,int(frame_size)):
            LS[i] = complex(np.log(Amp[i]+eps), Phs[i])
        Cep = np.real(scifft.ifft(LS)) # complex cepstrum
        Cep = np.squeeze(Cep)
        #CepA = np.real(scifft.ifft(np.log(Amp+eps)))
        
        # minimum phase : echo cancelled 
        #Cep_min = np.r_[1,2*np.ones(int(frame_size/2-1)),np.ones(1-frame_size%2),np.zeros(int(frame_size/2-1))]
        #Cep_min = Cep_min * CepA
        # source : higher quef, filter : lower quef
        Lifter = np.r_[np.ones(int(quef)),np.zeros(int(frame_size-2*quef)),np.ones(int(quef))]
        #Cep_H = Cep * Cep_min
        #Cep_H = Lifter * CepA
        Cep_H = Lifter * Cep
        Cep_Hs[0:int(quef),i_frame] = Cep_H[0:int(quef)]
        peak_count[i_frame] = len(signal.argrelmax(Cep_H[0:int(quef)],order=5)[0]) 
        if i_frame > wd:
            if sum(Pow[:,0]) < refPow:
                refPow = sum(Pow[:,0])
                ref_frame = i_frame
                #ref_Cep = Cep_H # Cep[0] is unnecessary ?
                    
        if i_frame > 0:
            #diffCep = (Cep_H - Cep_past)/2
            #diffLS = scifft.fft(diffCep)
            #diffXall = np.exp(diffLS)
            #diffX[:,i_frame-1] = diffXall[0:int(frame_size/2)] 
            XCep = np.correlate(Cep_H[2:int(quef)], Cep_past[2:int(quef)],"full")
            ACep = np.correlate(Cep_H[2:int(quef)], Cep_H[2:int(quef)],"full")
            ACep_past = np.correlate(Cep_past[2:int(quef)], Cep_past[2:int(quef)],"full")
            XCep = XCep/np.sqrt(ACep * ACep_past)
            #print(XCep.shape)
            CrossCep[i_frame-1] = np.nanmax(XCep)
            #CrossCep[i_frame-1] = XCep[int(quef-2)]
            
        Cep_past = Cep_H
                
        i_start = i_start + shift


    ref_Cep=np.mean(Cep_Hs[:,ref_frame-wd:ref_frame+wd],axis=1)
    CrossCep_ref = np.zeros([n_frame])
    i_start = 0
    while i_start + window_size - 1 < len_x - 1:
        x_now = np.zeros([frame_size,x.shape[1]])
        i_frame = int(i_start/shift)
        #print("%d\r",i_frame)
        i_end = min(i_start + window_size, len_x)
        x_now[0:int(i_end-i_start),:] = window * x[int(i_start):int(i_end),:]
        # Length FFT target should be window_size*2, latter points are zero-padding 
        X = scifft.fft(x_now)/frame_size
                
        # Inter-frame diff-quefrency pass filter for L 
        Amp = np.abs(X[:,0])
        Phs = np.unwrap(np.angle(X[:,0])*2)/2
        LS = np.zeros([int(frame_size),1],dtype=np.complex)
        for i in range(0,int(frame_size)):
            LS[i] = complex(np.log(Amp[i]+eps), Phs[i])
        Cep = np.real(scifft.ifft(LS)) # complex cepstrum
        Cep = np.squeeze(Cep)
        #CepA = np.real(scifft.ifft(np.log(Amp+eps)))
        # minimum phase : echo cancelled 
        #Cep_min = np.r_[1,2*np.ones(int(frame_size/2-1)),np.ones(1-frame_size%2),np.zeros(int(frame_size/2-1))]
        #Cep_min = Cep_min * CepA
        # source : higher quef, filter : lower quef
        Lifter = np.r_[np.ones(int(quef)),np.zeros(int(frame_size-2*quef)),np.ones(int(quef))]
        #Cep_H = Cep[:,0] - Lifter * Cep_min
        #Cep_H = Lifter * CepA
        Cep_H = Lifter * Cep
        
        XCep = np.correlate(Cep_H[2:int(quef)], ref_Cep[2:int(quef)],"full")
        ACep = np.correlate(Cep_H[2:int(quef)], Cep_H[2:int(quef)],"full")
        ACep_ref = np.correlate(ref_Cep[2:int(quef)], ref_Cep[2:int(quef)],"full")
        XCep = (XCep+eps)/(np.sqrt(ACep * ACep_ref)+eps)
        #print(np.nanmax(XCep))
        CrossCep_ref[i_frame] = np.nanmax(XCep) 
        #CrossCep_ref[i_frame] = XCep[int(quef-2)]
        i_start = i_start + shift
    
    
    return (peak_count, CrossCep,CrossCep_ref,ref_Cep,Cep_Hs,ref_frame)
    
        
