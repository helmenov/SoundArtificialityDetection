#%%
from scipy import fftpack
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.backends.backend_pdf import PdfPages

#%% Time series
Ts = 1/44100
x = [2.5, 2.0, 1.0, 2.5, 2.0, 1.0, 2.5, 2.0, 1.0, 2.5, 2.0, 1.0, 2.5, 2.0]
t = np.arange(0,len(x))*Ts*1000
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(t,x,'*-')
ax1.grid()
ax1.set_xlabel('Time [ms]')

#%% Windowing 
lenw = len(x)

#%%
b = lenw-len(x)
xx = np.zeros(lenw,)
xx[int(b/2):int(b/2)+len(x)]=np.array(x)
w = np.hanning(lenw+1)[:lenw]
x = w * xx
t = np.arange(len(x))*Ts*1000
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(t,x,'*-')
ax1.grid()
ax1.set_xlabel('Time [ms]')

#%% Mel-scaled Spectrum
# Mel = 2595*np.log10(1+f/700)


#%% Spectrum

LOG0 = 1

def rcunwrap(x):
    '''
        unwrap  the phase and removes phase corresponding to integer lag.
    '''
    n = len(x)
    nh = int(np.floor((n+1)/2))
    y = np.unwrap(x)
    nd = np.round((y[nh]/np.pi))
    for i in range(len(y)):
        y[i] = y[i] - np.pi*nd*i/nh
    return y, nd

def Ceps_Real(X):
    ncep = len(X)
    return np.real(fftpack.ifft(np.log(np.abs(X)+LOG0),ncep))

def Ceps_MinPhase(X):
    ncep = len(X)
    rceps = Ceps_Real(X)
    w = np.concatenate([[1], 2*np.ones((int(ncep/2-1),)), np.ones((int(1-ncep%2),)), np.zeros((int(ncep/2-1),))])
    return w * rceps

def MinPhased_Spectrum(Ceps_MinPhase):
    return np.exp(fftpack.fft(Ceps_MinPhase))

def Ceps_Complex(X):
    ncep = len(X)
    aX, nd = rcunwrap(np.angle(X))
    logh = np.log(np.abs(X)+LOG0)+1j*aX
    return np.real(fftpack.ifft(logh,ncep))

def Ceps_Allpass(X):
    ncep = len(X)
    return Ceps_Complex(X) - Ceps_MinPhase(X)

def ZeroPadding(x,N,tau):
    lenx = len(x)
    xx = np.zeros((N,))
    xx[tau:tau+lenx] = x
    return xx

def ZeroPaddingMid(x,N):
    '''
        fftshift(x,len(x))されたデータxを
        一旦ifftshift(len(x))したあとに
        Nuquistあたりにゼロパディングし，
        fftshift(xx,N)して返す
    '''
    lenx = len(x)
    xx = fftpack.ifftshift(x)
    n_pad = N-lenx
    xxx = np.concatenate([ xx[:int(lenx/2)], np.zeros((n_pad,)),xx[int(lenx/2):] ])
    xx = fftpack.fftshift(xxx)
    return xx

#%%

lamw = 2 # 
lam = 1 # 普通は ncep = nfft でどちらも2のべき乗

nfft = 2**int(np.ceil(np.log2(lamw*lenw)))

t = np.arange(nfft)*Ts*1000
f = np.arange(-nfft/2,nfft/2)/nfft/Ts/1000
f2 = np.arange(nfft)/nfft/Ts/1000

ncep = 2**int(np.ceil(np.log2(lam*nfft)))

q = np.arange(-ncep/2,ncep/2)/ncep*Ts/nfft*1000

fw = np.arange(-ncep/2,ncep/2)/nfft/Ts/1000


minphaselifter = np.zeros((ncep,))
minphaselifter[int(ncep/2)]=1
minphaselifter[int(ncep/2+1):]=2

fig = plt.figure(figsize=(15,15),dpi=72, tight_layout=True)
ax1 = fig.add_subplot(6,1,1)             # Time series
ax2 = fig.add_subplot(6,3,4)             # Magnitude Spectrum
ax3 = fig.add_subplot(6,3,7,sharex=ax2)  # Phase Spectrum
ax4 = fig.add_subplot(6,3,10)             # Magnitude Cepstrum
ax5 = fig.add_subplot(6,3,13,sharex=ax4)  # Minphase Cepstrum
ax6 = fig.add_subplot(6,3,16,sharex=ax4)  # allphase Cepstrum
ax7 = fig.add_subplot(6,3,8,sharex=ax2)  # rcPhase Spectrum
ax8 = fig.add_subplot(6,3,11,sharex=ax4)  # Magnitude Cepstrum
ax9 = fig.add_subplot(6,3,14,sharex=ax4)  # Minphase Cepstrum
ax10 = fig.add_subplot(6,3,17,sharex=ax4)  # allphase Cepstrum
ax11 = fig.add_subplot(6,3,6)
ax12 = fig.add_subplot(6,3,12)
ax13 = fig.add_subplot(6,3,15)
ax14 = fig.add_subplot(6,3,18)
ax15 = fig.add_subplot(6,3,9)

taustep = 8

for tau in range(0,nfft-len(x)+1,taustep):
    xx = np.zeros((nfft,))
    xx[tau:len(x)+tau] = x
    ax1.plot(t,xx+3*tau/taustep,'*-',label=repr(tau))

    X = fftpack.fft(xx)
    XX = fftpack.fftshift(X)
    ax2.plot(f2,10*np.log(np.real(X*np.conj(X))+LOG0),'*-',label=repr(tau))

    pX = np.angle(X)            # for non-shift
    pXX = fftpack.fftshift(pX) # for Shift

    pXX = np.unwrap(pXX)
    #pXX = pXX-pXX[int(nfft/2)]   # for shift
    pX1 = fftpack.ifftshift(pXX) # for non-shift
    ax3.plot(f2,pX1,'*-',label=repr(tau))
    lnX = np.log(np.abs(X))+ 1j*pX1

    C = fftpack.ifft(lnX,n=ncep)
    C = fftpack.ifftshift(C)
    Ca = np.real(C)
    ax4.plot(q,Ca+3*tau/taustep,'*-',label=repr(tau))
    # minphase
    Cm = minphaselifter * Ca
    ax5.plot(q,Cm+3*tau/taustep,'*-',label=repr(tau))
    # allpath
    Cal = C-Cm
    ax6.plot(q,np.abs(Cal)+3*tau/taustep,'*-',label=repr(tau))

    pXXr, nd = rcunwrap(pXX)
    #pXXr = pXXr-pXXr[int(nfft/2)]
    pXr = fftpack.fftshift(pXXr)
    ax7.plot(f2,pXr,'*-',label=repr(tau))

    lnX = np.log(np.abs(X))+ 1j*pXr
    C = fftpack.ifft(lnX,n=ncep)
    C = fftpack.ifftshift(C)
    Ca = np.real(C)
    ax8.plot(q,Ca+3*tau/taustep,'*-',label=repr(tau))
    # minphase
    Cm = minphaselifter * Ca
    ax9.plot(q,Cm+3*tau/taustep,'*-',label=repr(tau))
    # allpath
    Cal = C-Cm
    ax10.plot(q,np.abs(Cal)+3*tau/taustep,'*-',label=repr(tau))

    ###
    X2 = ZeroPaddingMid(XX,ncep)
    #X2 = ZeroPadding(XX,ncep,0)
    ax11.plot(fw,20*np.log(np.abs(X2)+LOG0),'*-', label=repr(tau))
    pX2, nd = rcunwrap(np.angle(X2))
    ax15.plot(fw,pX2,'*-',label=repr(tau))
    Ca = Ceps_Real(X2)
    Ca = fftpack.ifftshift(Ca)
    Cm = Ceps_MinPhase(X2)
    Cm = fftpack.ifftshift(Cm)
    Cal = Ceps_Allpass(X2)
    Cal = fftpack.ifftshift(Cal)
    ax12.plot(q,Ca+3*tau/taustep, '*-',label=repr(tau))
    ax13.plot(q,Cm+3*tau/taustep, '*-',label=repr(tau))
    ax14.plot(q,Cal+3*tau/taustep, '*-',label=repr(tau))
    

ax1.set_title('captured time series')
ax1.set_xlabel('Time [s]')
ax1.grid()
ax1.legend()

ax2.set_title('Magnitude Spectrum')
ax2.set_xlabel('Frequency [kHz]')
ax2.grid()
ax2.legend()

ax3.set_title('Phase Spectrum')
ax3.set_xlabel('Frequency[kHz]')
ax3.grid()
ax3.legend()

ax4.set_title('Real Cepstrum (Manual) without rcunwrap')
ax4.set_xlabel('Quefrency [ms]')
ax4.grid()
ax4.legend()

ax5.set_title('Minimum Cepstrum (Manual) without rcunwrap')
ax5.set_xlabel('Quefrency [ms]')
ax5.grid()
ax5.legend()

ax6.set_title('Allpass Cepstrum (Manual) without rcunwrap')
ax6.set_xlabel('Quefrency [ms]')
ax6.grid()
ax6.legend()


ax7.set_title('Phase-Spectrum (rcunwrap)')
ax7.set_xlabel('[kHz]')
ax7.grid()
ax7.legend()

ax8.set_title('Real-Cepstrum (Manual) with rcunwrap')
ax8.set_xlabel('Quefrency [ms]')
ax8.grid()
ax8.legend()

ax9.set_title('Minimum Cepstrum (Manual) with rcunwrap')
ax9.set_xlabel('Quefrency [ms]')
ax9.grid()
ax9.legend()

ax10.set_title('Allpass Cepstrum (Manual) without rcunwrap')
ax10.set_xlabel('Quefrency [ms]')
ax10.grid()
ax10.legend()

ax11.set_title('captured spectrum (not in dB)')
ax11.set_xlabel('Frequency [kHz]')
ax11.grid()
ax11.legend()

ax12.set_title('Real-Cepstrum (func) ')
ax12.set_xlabel('Quefrency [ms]')
ax12.grid()
ax12.legend()

ax13.set_title('Minimum Cepstrum (func)')
ax13.set_xlabel('Quefrency [ms]')
ax13.grid()
ax13.legend()

ax14.set_title('Allpass Cepstrum (func)')
ax14.set_xlabel('Quefrency [ms]')
ax14.grid()
ax14.legend()

plt.show()


#%%
# pdfファイルの初期化
#pdf = PdfPages('multipage.pdf')
# figureをセーブする
#pdf.savefig()
# pdfファイルをクローズする。
#pdf.close()

plt.savefig('saves.pdf',format='pdf',dpi=300)
# %%
