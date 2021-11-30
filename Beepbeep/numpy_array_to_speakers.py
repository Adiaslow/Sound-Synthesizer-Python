import numpy as np
import sounddevice as sd
import time

# Samples per second
sps = 44100

# Frequency / pith
freq_hz = 440.0

# Duration
duration_s = 5.0

# Attenuation so the sound is reasonable
atten = 0.3

# Waveform
each_sample_number = np.arange(duration_s * sps)
waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
waveform_quiet = waveform * atten

# Play the waveform
sd.play(waveform_quiet, sps)
time.sleep(duration_s)
sd.stop()