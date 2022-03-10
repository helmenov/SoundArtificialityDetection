# -*- coding: utf-8 -*-

__author__ = "Kotaro Sonoda <sonoda@cis.nagasaki-u.ac.jp>
__status__ = "production"
__version__ = "0.0.1"
__date__ = "05 December 2018"

import numpy as np
import matplotlib.pyplot as plt
import cis
import scipy.fftpack as sfft
import japanize_matplotlib
import matplotlib.mlab as mlab
import scipy.signal as ss

v,fs=cis.wavread('chocorate.wav')

window_size = 1024
v_pad = np.vstack([zeros((window_size,2)),v,zeros((windows_size/2,2))])
len_v=np.size(v_pad,1)
w_pad = zeros(len_v,1)


i_start = 1
while i_start+window_size-1<len_v :
    i_end = min(i_start+window_size-1,len_v)
    lv_now = sfft.fft(hanning(window_size)*v_pad[i_start:i_end,0]))
    rv_now = sfft.fft(hanning(window_size)*v_pad[i_start:i_end,1]))
    mlv_now = abs(lv_now)
    mrv_now = abs(rv_now)
    plv_now = angle(lv_now)
    prv_now = angle(rv_now)
    
    for i in range(1,window_size):
      if abs(plv_now(i) - prv_now(i)) < pi/18 :
        mcv_now(i) = min(mlv_now(i),mrv_now(i))
        pcv_now(i) = plv_now(i)
      else:
        mcv_now(i) = 0
        pcv_now(i) = 0
      cv_now(i) = mcv_now(i)*exp(pcv_now(i))

    w_pad[i_start:i_end]=w_pad[i_start:i_end] + sfft.ifft(cv_now)
    i_start = i_start+window_size/2

w = w_pad[window_size/2:len_v-window_size/2]
