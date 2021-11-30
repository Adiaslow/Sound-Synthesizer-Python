import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time

f_s = 44100
duration_s = 1.0
f_ca = 440.0
f_m1a = 0.0
f_m2a = 0.0
f_m3a = 0.0
k1a = 100.0
k2a = 100.0
k3a = 100.0


tis = np.arange(duration_s * f_s)
carriera = 2 * np.pi * tis * f_ca / tis
modulator1a = k1a * np.sin(2 * np.pi * tis * f_m1a / f_s)
modulator2a = k2a * np.sin(2 * np.pi * tis * f_m2a / f_s)
modulator3a = k3a * np.sin(2 * np.pi * tis * f_m3a / f_s)

osc1_output = carriera + modulator1a + modulator2a + modulator3a

waveform = np.cos(osc1_output)

waveform_quiet = waveform * 0.3
waveform_integers = np.int16(waveform_quiet * 32767)
write('fm_out.wav', f_s, waveform_integers)

sd.play(waveform_quiet, f_s)
time.sleep(duration_s)
sd.sleep()