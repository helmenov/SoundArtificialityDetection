#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 21:11:19 2020

@author: kotaro
"""
import numpy as np
from scipy import fftpack as scifft

def cepstrum(x, padding_ratio, fs, window='true'):
    '''
    
    Parameters
    ----------
    x : TYPE
        time-series data
    padding_ratio :
        integer size ratio of analyzing frame to x
    fs : Sampling Frequency [Hz] 
    mode : TYPE, optional
        DESCRIPTION. The default is 'complex'.
    window : 
        The default is 'True'

    Returns
    -------
    cepstrum

    '''    

    eps = 1e-15
    # x is (len_x,ch_x)-shape matrix
    len_x = x.shape[0]
    ch_x = x.shape[1]
    
    # windowing
    if window:
        #w = (np.hanning(len_x + 1))[:len_x].reshape([len_x,1]) # periodic or shift-add 
        w = (np.hanning(len_x))[:len_x].reshape([len_x,1]) # else
    else:
        w = np.ones([len_x,1])
    x = w * x
    
    # framing (zero-padding)
    len_frame = padding_ratio * len_x
    xx = np.zeros([len_frame,ch_x])
    xx[:len_x] = x
    
    ## fourier transform (complex) X[0] is sum, not mean. In case of ifft ,results are mean (sum devided length)
    X = scifft.fft(xx,axis=0)/len_x
    X = scifft.fftshift(X)
    freq = scifft.fftshift(scifft.fftfreq(len_frame,d=1/fs))
    
    
    ## Amplitude and Phase Spectrum (both real) <- popular 
    Xa = np.real(np.sqrt(X * np.conj(X)))
    Xp = np.zeros([len_frame,ch_x])
    Xp[int(len_frame/2):,0] = np.real(np.unwrap(np.angle(X[int(len_frame/2):,0])*2)/2)
    minusfreq = np.angle(X[:int(len_frame/2-1),0])
    minusfreq = np.append(minusfreq,[0])
    minusfreq = np.flipud(minusfreq)
    minusfreq = np.unwrap(minusfreq*2)/2
    minusfreq = np.flipud(minusfreq)
    Xp[:int(len_frame/2-1),0] = minusfreq[0:int(len_frame/2-1)]
    
    ## Log Spectrum 
    LnXa = np.log(Xa+eps)
    LnXp = Xp
    
    ## Log Spectrum (complex)
    LnX = np.zeros([len_frame,ch_x],dtype=np.complex)
    for i in range(0,int(len_frame)):
        LnX[i,0] = np.complex(LnXa[i,0], LnXp[i,0])
    
    ## Before Calculating cepstrum, input should be subtracted by LnX[0] ? 
    
    ## Cepstrum (real, asynmetric)
    C = np.real(scifft.fft(LnX,axis=0))/len_frame
    C = scifft.ifftshift(C)
    quef = scifft.ifftshift(scifft.fftfreq(len_frame,d=fs))
        
    ## Cepstrum (amplitude) (real, even)  = abs cepstrum
    Ca = np.real(scifft.fft(np.real(LnX),axis=0))/len_frame
    Ca = scifft.ifftshift(Ca)
    
    ## Cepstrum (phase) (real, odd)
    Cp = np.real(scifft.fft(np.imag(LnX),axis=0))/len_frame
    Cp = scifft.ifftshift(Cp)
    
    ## Cepstrum (minimum-pahse) (real, asynmetric)
    Cmin = np.zeros([len_frame,ch_x])
    Cmin[int(len_frame/2):] = 2 * Ca[int(len_frame/2):]
    # if odd, Cmin[int(len_frame+1)/2] = Ca[int(len_frame+1)/2]
    
    ## Cepstrum (all-path) (real, asynmetric)
    Call = C - Cmin
    
    ## Log spectrum (minimum-phase) (complex)
    LnXmin = scifft.fft(Cmin,axis=0)
    LnXmin = scifft.fftshift(LnXmin)
    
    ## Log Spectrum (all-path) (complex)
    LnXall = scifft.fft(Call,axis=0)
    LnXall = scifft.fftshift(LnXall)
    
    ## Spectrum (minimum-phase) (complex)
    Xmin = np.exp(LnXmin)
    
    ## Spectrum (all-path) (complex)
    Xall = np.exp(LnXall)
    
    ## Time-series (minimum-phase) 
    xmin = scifft.fft(Xmin,axis=0)/len_frame
    xmin = scifft.ifftshift(xmin)
    
    ## Time-series (minimum-phase)
    xall = scifft.fft(Xall,axis=0)/len_frame
    xall = scifft.ifftshift(xall)
    
    ### time-series
    ## x = xmin + xall
    
    ### Fourier-domain
    ## X  Xmin     Xall
    ## Xa Xa,min   Xa,all(=1) 
    ## Xp Xp,min   Xp,all
    Xamin = np.real(Xmin)
    Xaall = np.real(Xall)
    Xpmin = np.imag(Xmin)
    Xpall = np.imag(Xall)
    
    ### Cepstrum-domain
    ## C  Cmin  Call
    ## Ca Camin Caall(=0)
    ## Cp Cpmin Cpall
    Camin = Ca
    Caall = np.zeros([len_frame,ch_x],dtype=np.complex)
    Cpmin = Cmin-Camin
    Cpall = Call
    
    return x,xmin,xall,X,Xmin,Xall,Xa,Xamin,Xaall,Xp,Xpmin,Xpall,C,Cmin,Call,Ca,Camin,Caall,Cp,Cpmin,Cpall,freq,quef

def main():
    x, fs = sf.read(fname)
    len_x = x.shape[0]
    num_ch = x.shape[1]

    # define frame window

    # short-term fft
    i_start = 0
    n_frame = int(np.floor(len_x/shift))

    
if __name__ == '__main__': main()

