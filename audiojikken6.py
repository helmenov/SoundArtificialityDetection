# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 15:49:00 2018

@author: Yasuhiro Kuroda
"""

import numpy as np
import matplotlib.pyplot as plt
import cis
import scipy.fftpack as sfft
import japanize_matplotlib
import matplotlib.mlab as mlab
import scipy.signal as ss

def convert_monoralL(vin):
    vout = vin
    if  (vin.ndim) >1:#字数が1より大きいとき、1列目だけを取り出す（ステレオ音対策）
        vout=vin[:,0]
        print("reshaped")
    else:
        print("not reshape")
    return vout
def convert_monoralR(vin):
    vout = vin
    if  (vin.ndim) >1:#字数が1より大きいとき、1列目だけを取り出す（ステレオ音対策）
        vout=vin[:,1]
        print("reshaped")
    else:
        print("not reshape")
    return vout

def sfft_vin(vin,i,j):#i=始まり、j=終わり
    vs =sfft.fft(vin[i:j]*np.hanning(1024))
    #r=np.arange(200)
    """
    plt.subplot(3,3,1)
    plt.plot(np.abs(vs[:512]))#振幅スペクトル
    plt.ylabel("vsの振幅スペクトル")
    plt.subplot(3,3,2)
    plt.plot(np.angle(vs[:512]))#位相スペクトル
    plt.ylabel("vsの位相スペクトル")
    plt.subplot(3,3,3)
    plt.plot(np.unwrap(np.angle(vs[:512])))
    plt.ylabel("vsの位相スペクトルunwrap")
    """
    return vs

def soukan(vsin1,vsin2):
    vs2conj=np.conj(vsin2)
    vsPower=vsin1*vs2conj 
    vsPoweridft=sfft.ifft(vsPower)
    
    """
    plt.subplot(3,3,4)
    plt.plot(np.abs(vs2conj[:512]))#振幅スペクトル
    plt.ylabel("vs2conjの振幅スペクトル")
    plt.subplot(3,3,5)
    plt.plot(np.angle(vs2conj[:512]))#位相スペクトル
    plt.ylabel("vs2conjの位相スペクトル")
    plt.subplot(3,3,6)
    plt.plot(np.unwrap(np.angle(vs2conj[:512])))
    plt.ylabel("vs2conjの位相スペクトルunwrap")
    
    plt.subplot(3,3,7)
    plt.plot(vsPower[:512])#パワースペクトル
    plt.ylabel("vsのパワースペクトル")
    plt.subplot(3,3,8)
    """
    plt.plot(vsPoweridft[:1024])#自己相関
    plt.ylabel("vsの自己相関関数")
    """
    plt.subplot(3,3,9)
    plt.plot(v1[:1024])#音声波形
    plt.ylabel("音声波形v")
    """
#input wavfile    
v1 , fs1=cis.wavread('chocorate.wav')
v2,fs2 =cis.wavread('chocorate.wav')

print('v1の次元数は'+str(v1.ndim))
print('v2の次元数は'+str(v2.ndim))

v1=convert_monoralL(v1)
v2=convert_monoralR(v2)
    
"""配列定義の文法チェック
c=np.array([[1,3,5,6,7],[5,5,7,23,4]])
c=c[1,:]
print(c)
"""

"""
t = np.arange(0,3,1/fs1)
f=440
a = 0.1
ysin=a*np.sin(2*np.pi*f*t)
print(v.shape)
print(ysin.shape)

vmix=v[0:np.size(t)]+ysin+a*np.sin(2*np.pi*2*f*t)
cis.audioplay(vmix[:np.size(t)],fs)
cis.wavwrite("output.wav",vmix,fs)
"""
"""ボーカル抜く作業
t = np.arange(0,30,1/fs1)
v3=v1-v2
v4=v2-v3

cis.audioplay(v4[:np.size(t)],fs1)


framelength=1024#フレーム長

"""
cis.audioplay(v1[:1024],fs1)


vs1=sfft_vin(v1,10000,11024)
vs2=sfft_vin(v2,10000,11024)


soukan(vs1,vs2)
soukan(vs1,vs1)
soukan(vs2,vs2)
plt.show()
