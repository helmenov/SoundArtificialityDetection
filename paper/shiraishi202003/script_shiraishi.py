#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:44:00 2020
@author: kotaro
"""

import replay_sensor
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np

#plt.style.use('kotaro')

#WavHome = "/opt/LivenessEvaluationSoundsDataset/"
#WavHome = "c:/Users/akari/Documents/PA/PA/ASVspoof2019_PA_dev/flac1/"
WavHome = "c:/Users/akari/Documents/Audacity/Audacity3/"

window_size = 4096 # 8192
frame_size = 4096
shift = int(window_size/2)


labelname = ["","","",""]
#wavname = ["0001.flac","5401.flac","5603.flac","5805.flac"]
#wavname = ["0011.flac","5422.flac","5624.flac","5826.flac"]
wavname = ["0051.flac","5502.flac","5704.flac","5906.flac"]
#wavname = ["PA_D_0000001.flac","PA_D_0005401.flac","PA_D_0005603.flac","PA_D_0005805.flac"]

labellist = ['bonafide','spoof-perfect','spoof-high','spoof-low']


for i, p in enumerate(wavname, 0): 
    wavname_path = WavHome+p
    x, fs = sf.read(wavname_path)
    x = x.reshape([len(x),x.ndim])
    x = x[:,0]
    
    len_x = len(x)
    quef = int(window_size/2) #32    
    n_frame = int(np.floor(len_x/shift))
    Cep_Hs = np.zeros([6,quef,n_frame])
    min_frame = np.zeros([6,])
    
    q = (np.arange(int(frame_size/2))/fs)[:int(quef)]

    peak_count,  Cep_Hs[i,:,:] = replay_sensor.replay_sensor(wavname_path,window_size,frame_size,shift)

    fig = plt.figure(figsize=(10,10),dpi=60)
    fig.subplots_adjust(hspace=0.5)
    
    # fig(a) time-series
    ax1 = fig.add_subplot(2,1,1)
    t1 = np.arange(len_x)/fs
    ax1.plot(t1,x)
    ax1.set_xlabel('Time [s]')
    ax1.grid(which='minor')
    ax1.set_title(labellist[i])
    ax1.set_rasterized('True')
    
    # fig(b) CrossCep_ref
    ax2 = fig.add_subplot(2,1,2)
    t2 = np.arange(len(peak_count))*shift/fs
    ax2.plot(t2[:-1],peak_count[:-1])
    ax2.grid(which='minor')
    ax2.set_title("Number of Cepstrum Peaks")
    ax2.set_xlabel("Time [s]")
    ax2.sharex(ax1)
    # ax2.set_ylim([0, 2])
    ax2.set_rasterized('True')
        
    plt.show()
    fig.savefig("%03.f"%(i)+'.png', bbox_inches="tight", pad_inches=0.05)

    
    # cepstrum of 5,15,25,35 second
    fig2 = plt.figure(figsize=(10,10),dpi=60)
    fig2.subplots_adjust(hspace=0.5)
    
    '''
    #69
    ax21 = fig2.add_subplot(4,1,1)
    iframe = int(0.4*fs/shift)
    ax21.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.4[s]')
    ax21.set_xlabel('Quefrency [s]')
    ax21.set_ylim([-50, 50])
    ax21.grid(which="major")
    ax21.set_title(labellist[i])
    ax21.legend()
    ax21.set_rasterized('True')
    
    ax22 = fig2.add_subplot(4,1,2)
    iframe = int(0.5*fs/shift)
    #ax22.plot(Cep_Hs[i,2:,iframe])
    ax22.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.5[s]')
    ax22.set_xlabel('Quefrency [s]')
    ax22.set_ylim([-50, 50])
    ax22.grid(which="major")
    ax22.set_title(labellist[i])
    ax22.legend()
    ax22.set_rasterized('True')
    
    ax23 = fig2.add_subplot(4,1,3)
    iframe = int(0.9*fs/shift)
    #ax23.plot(Cep_Hs[i,2:,iframe])
    ax23.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.9[s]')
    ax23.set_xlabel('Quefrency [s]')
    ax23.set_ylim([-50, 50])
    ax23.grid(which="major")
    ax23.set_title(labellist[i])
    ax23.legend()
    ax23.set_rasterized('True')
    
    ax24 = fig2.add_subplot(4,1,4)
    iframe = int(1.3*fs/shift)
    #ax24.plot(Cep_Hs[i,2:,iframe])
    ax24.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  1.3[s]')
    ax24.set_xlabel('Quefrency [s]')
    ax24.set_ylim([-50, 50])
    ax24.grid(which="major")
    ax24.set_title(labellist[i])
    ax24.legend()
    ax24.set_rasterized('True')
    
    '''   
    '''
    #70
    ax21 = fig2.add_subplot(4,1,1)
    iframe = int(0.1*fs/shift)
    #ax21.plot(Cep_Hs[i,2:,iframe])
    ax21.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.1[s]')
    ax21.set_xlabel('Quefrency [s]')
    ax21.set_ylim([-50, 50])
    ax21.grid(which="major")
    ax21.set_title(labellist[i])
    ax21.legend()
    ax21.set_rasterized('True')
    
    ax22 = fig2.add_subplot(4,1,2)
    iframe = int(0.2*fs/shift)
    #ax22.plot(Cep_Hs[i,2:,iframe])
    ax22.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.2[s]')
    ax22.set_xlabel('Quefrency [s]')
    ax22.set_ylim([-50, 50])
    ax22.grid(which="major")
    ax22.set_title(labellist[i])
    ax22.legend()
    ax22.set_rasterized('True')
    
    ax23 = fig2.add_subplot(4,1,3)
    iframe = int(0.5*fs/shift)
    #ax23.plot(Cep_Hs[i,2:,iframe])
    ax23.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.5[s]')
    ax23.set_xlabel('Quefrency [s]')
    ax23.set_ylim([-50, 50])
    ax23.grid(which="major")
    ax23.set_title(labellist[i])
    ax23.legend()
    ax23.set_rasterized('True')
    
    ax24 = fig2.add_subplot(4,1,4)
    iframe = int(0.9*fs/shift)
    #ax24.plot(Cep_Hs[i,2:,iframe])
    ax24.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.9[s]')
    ax24.set_xlabel('Quefrency [s]')
    ax24.set_ylim([-50, 50])
    ax24.grid(which="major")
    ax24.set_title(labellist[i])
    ax24.legend()
    ax24.set_rasterized('True')

    '''
    #74
    ax21 = fig2.add_subplot(4,1,1)
    iframe = int(0.4*fs/shift)
    #ax21.plot(Cep_Hs[i,2:,iframe])
    ax21.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  0.4[s]')
    ax21.set_xlabel('Quefrency [s]')
    ax21.set_ylim([-50, 50])
    ax21.grid(which="major")
    ax21.set_title(labellist[i])
    ax21.legend()
    ax21.set_rasterized('True')
   
    ax22 = fig2.add_subplot(4,1,2)
    iframe = int(1.1*fs/shift)
    #x22.plot(Cep_Hs[i,2:,iframe])
    ax22.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  1.1[s]')
    ax22.set_xlabel('Quefrency [s]')
    ax22.set_ylim([-50, 50])
    ax22.grid(which="major")
    ax22.set_title(labellist[i])
    ax22.legend()
    ax22.set_rasterized('True')
    
    ax23 = fig2.add_subplot(4,1,3)
    iframe = int(1.2*fs/shift)
    #ax23.plot(Cep_Hs[i,2:,iframe])
    ax23.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  1.2[s]')
    ax23.set_xlabel('Quefrency [s]')
    ax23.set_ylim([-50, 50])
    ax23.grid(which="major")
    ax23.set_title(labellist[i])
    ax23.legend()
    ax23.set_rasterized('True')
    
    ax24 = fig2.add_subplot(4,1,4)
    iframe = int(2.0*fs/shift)
    #ax24.plot(Cep_Hs[i,2:,iframe])
    ax24.plot(q[2:],Cep_Hs[i,2:,iframe],label='Cepstrum in  2.0[s]')
    ax24.set_xlabel('Quefrency [s]')
    ax24.set_ylim([-50, 50])
    ax24.grid(which="major")
    ax24.set_title(labellist[i])
    ax24.legend()
    ax24.set_rasterized('True')

    plt.show()
    fig2.savefig(labelname[i]+'_ceps.png', bbox_inches="tight", pad_inches=0.05)
    
    
lslist = ['-',':','-.','--']
markerlist = ['s','o','d','x']
plt.figure(3)    
peak_average = list()
# fig(b) CrossCep_ref
for i, p in enumerate(wavname, 0): 
    wavname_path = WavHome+p
    x, fs = sf.read(wavname_path)
    x = x.reshape([len(x),x.ndim])
    x = x[:,0]
    
    len_x = len(x)
    quef = int(window_size/2) #32    
    n_frame = int(np.floor(len_x/shift))
    Cep_Hs = np.zeros([6,quef,n_frame])
    min_frame = np.zeros([6,])

    
    peak_count,  Cep_Hs[i,:,:] = replay_sensor.replay_sensor(wavname_path,window_size,frame_size,shift)

    t2 = np.arange(len(peak_count))*shift/fs
    plt.plot(t2[:-1],peak_count[:-1],ls = lslist[i],marker= markerlist[i],label=labellist[i])        
    #plt.show()
    
    peak_value = 0
    j = 0
    number = 0
    for j in peak_count:
        peak_value = peak_value + j
        number += 1
    
    peak_value = peak_value/number#平均
    
    peak_average.append(peak_value)
    
print(peak_average)
plt.grid(True)
plt.title("Number of Cepstrum Peaks")
plt.xlabel("Time [s]")
#plt.ylim([0, 2])
plt.legend()
plt.savefig('ceps.png', bbox_inches="tight", pad_inches=0.05)


plt.figure(4) 
plt.grid(True)
plt.rcParams['axes.axisbelow'] = True
left = np.array([1, 2, 3, 4])
label = ["bonafide", "spoof-perfect", "spoof-high","spoof-low"]
colorlist = ['b', 'darkorange','g','r']
plt.bar(left, peak_average, label=label, align="center", color=colorlist)
#plt.set_ylim(bottom=160, top=180)  # y範囲
#plt.legend()
plt.xticks(left, label)
plt.ylim(170,175)
plt.show()

#plt.savefig('ave.png', bbox_inches="tight", pad_inches=0.05)