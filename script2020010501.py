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

plt.style.use('kotaro')

WavHome = "/opt/LivenessEvaluationSoundsDataset/"

window_size = 1024 
frame_size = 8192
shift = 128

labelname = ["live", "env", "concat", "mix", "pops", "jazz"]
wavname = ["01live.wav", "02eki.wav", "03concat.wav", "04mix.wav", "05pops.wav", "06jazz.wav"]

for i, p in enumerate(wavname, 0): 
    wavname_path = WavHome+p
    x, fs = sf.read(wavname_path)
    x = x[:,0]
    len_x = len(x)
    CrossCep, CrossCep_ref, ref_Cep = liveness_sensor.liveness_sensor(wavname_path,window_size,frame_size,shift)

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
    t2 = np.arange(len(CrossCep_ref))*shift/fs
    ax2.plot(t2,CrossCep_ref)
    ax2.grid(which='minor')
    ax2.set_title("Cross-Correlation Coefficients")
    ax2.set_xlabel("Time [s]")
    ax2.set_rasterized('True')

    plt.show()
    fig.savefig(labelname[i]+'.pdf', bbox_inches="tight", pad_inches=0.05)
    