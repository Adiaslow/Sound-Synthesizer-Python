import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time
import matplotlib.pyplot as plt

f_s = 44100
duration_s = 2.0

square_wave_a = False
f_ca = 440.0
oct1 = 1
amp1 = 0.05
f_m1a = 220.0
f_m2a = 440.0
f_m3a = 880.0
k1a = 0.0
k2a = 0.0
k3a = 0.0

square_wave_b = False
f_cb = 587.33
oct2 = 1
amp2 = 0.05
f_m1b = 0.0
f_m2b = 0.0
f_m3b = 0.0
k1b = 0.0
k2b = 0.0
k3b = 0.0

square_wave_c = False
f_cc = 783.99
oct3 = 1
amp3 = 0.0
f_m1c = 0.0
f_m2c = 0.0
f_m3c = 0.0
k1c = 0.0
k2c = 0.0
k3c = 0.0

scope_scale = 0.25

tis = np.arange(duration_s * f_s)

print(len(tis), 'Samples')

# Oscillators
# 1
carrier_a = 2 * np.pi * f_ca * tis / f_s

modulator1a = k1a * np.sin(2 * np.pi * tis * f_m1a / f_s)
modulator2a = k2a * np.sin(2 * np.pi * tis * f_m2a / f_s)
modulator3a = k3a * np.sin(2 * np.pi * tis * f_m3a / f_s)

if (f_m1a <= 0):
    osc1 = carrier_a * oct1
else:
    osc1 = (carrier_a + modulator1a + modulator2a + modulator3a)

# 2
carrier_b = 2 * np.pi * tis * f_cb / f_s

modulator1b = k1b * np.sin(2 * np.pi * tis * f_m1b / f_s)
modulator2b = k2b * np.sin(2 * np.pi * tis * f_m2b / f_s)
modulator3b = k3b * np.sin(2 * np.pi * tis * f_m3b / f_s)

if (f_m1b <= 0):
    osc2 = carrier_b * oct2
else:
    osc2 = (carrier_b + modulator1b + modulator2b + modulator3b)
    
# 3
carrier_c = 2 * np.pi * tis * f_cc / f_s

modulator1c = k1c * np.sin(2 * np.pi * tis * f_m1c / f_s)
modulator2c = k2c * np.sin(2 * np.pi * tis * f_m2c / f_s)
modulator3c = k3c * np.sin(2 * np.pi * tis * f_m3c / f_s)

if (f_m1b <= 0):
    osc3 = carrier_c * oct3
else:
    osc3 = (carrier_c + modulator1c + modulator2c + modulator3c)
    

new_waveform = (np.sin(osc1) * amp1) + (np.sin(osc2) * amp2) + (np.sin(osc3) * amp3)

waveform_quiet = new_waveform * 1
waveform_integers = np.int16(waveform_quiet * 32767)
write('fractal_synth', f_s, waveform_integers)

# Plots

fig, (ax1, ax2) = plt.subplots(1, 2)

fig.suptitle("Signal Analysis", y=1.04)

ax1.plot(waveform_quiet)
ax1.set_title("Oscilloscope")
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Amplitude (linear)')
ax1.set_xlim([0,500])
ax1.set_ylim([-scope_scale , scope_scale])

ax2.specgram(waveform_quiet,Fs = f_s, NFFT = 1024, scale_by_freq = True)
ax2.set_title("Spectrogram")
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Frequency (hz)')
ax2.set_ylim([0,10000])

fig.tight_layout()
plt.show()

# Play signal
sd.play(waveform_quiet, f_s)
time.sleep(duration_s)
sd.sleep(round(duration_s))
