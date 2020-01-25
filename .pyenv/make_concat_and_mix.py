#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 02:59:12 2020

@author: kotaro
"""

import soundfile as sf
import numpy as np

labelname = ["live", "env", "concat", "mix", "pops", "jazz"]
wavname = ["01live.wav", "02eki.wav", "03concat.wav", "04mix.wav", "05pops.wav", "06jazz.wav"]

p0 = wavname[0]
wavname_path0 = WavHome+p0
live, fs = sf.read(wavname_path0)
live = live/np.std(live)

p1 = wavname[1]
wavname_path1 = WavHome+p1
env, fs = sf.read(wavname_path1)
env = env/np.std(env)

start = int(live.shape[0]/2)
length = int(live.shape[0])

concat = np.concatenate([live,env])
concat = concat[start:int(start+length),:]
concat = 0.9*concat/np.max(abs(concat))

p2 = wavname[2]
wavname_path2 = WavHome+p2
sf.write(wavname_path2,concat,fs)

mix_start = int(env.shape[0]/4)
mix_end = int(env.shape[0]*3/4)
live_m = np.zeros(live.shape)
live_m[mix_start:mix_end,:] = live[mix_start:mix_end,:]
mix = env + live_m
mix = 0.9*mix/np.max(abs(mix))

p3 = wavname[3]
wavname_path3 = WavHome+p3
sf.write(wavname_path3,mix,fs)


from matplotlib import pyplot as plt
fig = plt.figure(figsize=(10,10),dpi=60)
fig.subplots_adjust(hspace=1.2)
ax1 = fig.add_subplot(4,1,1)
ax1.plot(live[:,0])
ax1.set_ylim(-7,7)
ax2 = fig.add_subplot(4,1,2)
ax2.plot(env[:,0])
ax2.set_ylim(-7,7)
ax3 = fig.add_subplot(4,1,3)
ax3.plot(concat[:,0])
ax3.set_ylim(-7,7)
ax4 = fig.add_subplot(4,1,4)
ax4.plot(mix[:,0])
ax4.set_ylim(-7,7)

