#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 20:00:33 2020

@author: kotaro
"""
import numpy as np
from scipy import fftpack as scifft 
from matplotlib import pyplot as plt

eps = 1e-10
Fs = 44100 # [Hz] Fs points per 1 second   
LenFrame = 2**9


SampleSize = 2**9 # [points]   
SampleTime0 = int(SampleSize/2)

# data
F0freq = 9000 # [Hz]
F0amp = np.exp(1) # jikkouchi 
DCamp = 0 #np.exp(2)

# fig
fig = plt.figure(figsize=(10,10),dpi=60)
fig.subplots_adjust(hspace=1.2)



# sample
t = np.linspace(start=-SampleTime0,stop=SampleSize-SampleTime0,num=SampleSize,endpoint=False)/Fs
DCwave = DCamp * np.ones(t.shape)
F0wave = F0amp * np.sin(2*np.pi*F0freq*t)
wave = DCwave + F0wave

# plot
ax1 = fig.add_subplot(5,1,1)
ax1.plot(t,wave)
ax1.grid(which='major')
ax1.set_title("Time-series")
ax1.set_rasterized('True')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Magnitude')

# Windowing 
win = np.hanning(SampleSize+1)[:SampleSize] # hanning
#win = np.ones([SampleSize,]) # rectangular
ax2 = fig.add_subplot(5,1,2)
ax2.plot(t,win)
ax2.grid(which='major')
ax2.set_title("Time-series")
ax2.set_rasterized('True')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Weight')
ax2.set_ylim(-0.1,1.1)

# anlyzed frame (time 0 is frame-center)
x = np.zeros([LenFrame,])
tx = np.linspace(start=-int(LenFrame/2),stop=int(LenFrame/2),num=LenFrame,endpoint=False)/Fs
for i in range(0,LenFrame):
    for j in range(0,SampleSize):
        if ((tx[i]-t[j])**2 < eps):
            x[i] = win[j]*wave[j]

ax3 = fig.add_subplot(5,1,3)
ax3.plot(tx,x)
ax3.grid(which='major')
ax3.set_title("Time-series")
ax3.set_rasterized('True')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Magnitude')

# Fourier Transform
X = scifft.fft(x)/(LenFrame*sum(win/SampleSize))
f = scifft.fftfreq(n=LenFrame,d=1/Fs)

LogX = np.log(X+eps)


f_shift = scifft.fftshift(f)
LogX_shift = scifft.fftshift(LogX)
MagLogX = np.real(LogX_shift)
Phase = np.unwrap(2*np.imag(LogX_shift))/2
Phase = Phase - 2*np.pi* (Phase[int(LenFrame/2)]//(2*np.pi))

ax4 = fig.add_subplot(5,2,7)
ax4.plot(f_shift,MagLogX)
ax4.grid(which='major')
ax4.set_title("Realpart of LogSPectrum")
ax4.set_rasterized('True')
ax4.set_xlabel('Frequency [Hz]')
ax4.set_ylabel('Magnitude')

ax5 = fig.add_subplot(5,2,8)
ax5.plot(f_shift,Phase)
ax5.grid(which='major')
ax5.set_title("Imaginary of LogSpectrum (Phase)")
ax5.set_rasterized('True')
ax5.set_xlabel('Frequency [Hz]')
ax5.set_ylabel('Phase')

# -freq -> +freq
MagLogX[:int(LenFrame/2)] = 0
MagLogX[int(LenFrame/2+1):] = 2*MagLogX[int(LenFrame/2+1):]


# Cepstrum
C = scifft.ifft(LogX)
C_shift = scifft.ifftshift(C)
q_shift = scifft.ifftshift(scifft.fftfreq(n=LenFrame,d=Fs/LenFrame))

ax6 = fig.add_subplot(5,2,9)
ax6.plot(q_shift,np.real(C_shift))
ax6.grid(which='major')
ax6.set_title("Realpart of Cepstrum")
ax6.set_rasterized('True')
ax6.set_xlabel('Quefrency [s]')
ax6.set_ylabel('Realpart')

ax7 = fig.add_subplot(5,2,10)
ax7.plot(q_shift,np.imag(C_shift))
ax7.grid(which='major')
ax7.set_title("Imaginary of Cepstrum")
ax7.set_rasterized('True')
ax7.set_xlabel('Quefrency [s]')
ax7.set_ylabel('Imaginarypart')
ax7.set_ylim(-1,1)
