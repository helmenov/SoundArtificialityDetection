#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:44:00 2020

@author: kotaro
"""
import liveness_sensor
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np

#plt.style.use('kotaro')

#WavHome = "/opt/LivenessEvaluationSoundsDataset/"
WavHome = "c:/Users/Kotaro/My Repository/SoundArtificialityDetection/wavs/"

window_size = 8192
frame_size = 8192
shift = int(window_size/2)

labelname = ["live", "env", "concat", "mix", "pops", "jazz"]
wavname = ["01live.wav", "02eki.wav", "03concat.wav", "04mix.wav", "05pops.wav", "06jazz.wav"]
n_frame = int(np.floor(1764000/shift))
quef = int(window_size/8)
Cep_Hs = np.zeros([6,quef,n_frame])
ref_Cep = np.zeros([6,quef]) 
min_frame = np.zeros([6,])
for i, p in enumerate(wavname, 0): 
    wavname_path = WavHome+p
    x, fs = sf.read(wavname_path)
    x = x[:,0]
    len_x = len(x)
    CrossCep, CrossCep_ref, ref_Cep[i,:], Cep_Hs[i,:,:], min_frame[i] = liveness_sensor.liveness_sensor(wavname_path,window_size,frame_size,shift)

    fig = plt.figure(figsize=(10,10),dpi=60)
    fig.subplots_adjust(hspace=0.5)
    
    # fig(a) time-series
    ax1 = fig.add_subplot(2,1,1)
    t1 = np.arange(len_x)/fs
    ax1.plot(t1,x)
    ax1.grid(which='minor')
    ax1.set_title("Time-series")
    ax1.set_rasterized('True')
    
    # fig(b) CrossCep_ref
    ax2 = fig.add_subplot(2,1,2)
    t2 = np.arange(len(CrossCep_ref)-30)*shift/fs
    ax2.plot(t2,CrossCep_ref[0:n_frame-30])
    ax2.grid(which='minor')
    ax2.set_title("Cross-Correlation Coefficients")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylim([0.8, 1.2])
    ax2.set_rasterized('True')

    plt.show()
    fig.savefig(labelname[i]+'.png', bbox_inches="tight", pad_inches=0.05)
    
    # cepstrum of 5,15,25,35 second
    fig2 = plt.figure(figsize=(10,10),dpi=60)
    fig2.subplots_adjust(hspace=0.5)
    
    ax21 = fig2.add_subplot(4,1,1)
    iframe = int(5*fs/shift)
    ax21.plot(Cep_Hs[i,2:,iframe])
    ax21.grid(which="major")
    ax21.set_title("Cepstrum in 5[s]")
    ax21.set_rasterized('True')
    
    ax22 = fig2.add_subplot(4,1,2)
    iframe = int(15*fs/shift)
    ax22.plot(Cep_Hs[i,2:,iframe])
    ax22.grid(which="major")
    ax22.set_title("Cepstrum in 15[s]")
    ax22.set_rasterized('True')
    
    ax23 = fig2.add_subplot(4,1,3)
    iframe = int(25*fs/shift)
    ax23.plot(Cep_Hs[i,2:,iframe])
    ax23.grid(which="major")
    ax23.set_title("Cepstrum in 25[s]")
    ax23.set_rasterized('True')
    
    ax24 = fig2.add_subplot(4,1,4)
    iframe = int(35*fs/shift)
    ax24.plot(Cep_Hs[i,2:,iframe])
    ax24.grid(which="major")
    ax24.set_title("Cepstrum in 35[s]")
    ax24.set_rasterized('True')
    
    plt.show()
    fig2.savefig(labelname[i]+'_ceps.png', bbox_inches="tight", pad_inches=0.05)
    
    
    