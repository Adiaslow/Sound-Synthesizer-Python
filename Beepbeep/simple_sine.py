# Import
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Properties of the wav
sps = 44100
carrier_hz = 440.0
duration_s = 10.0

# Calculate the sine wive
t_samples = np.arange(sps * duration_s)
carrier = np.sin(2 * np.pi * carrier_hz * t_samples / sps)
carrier *= 1
carrier_ints = np.int16(carrier * 32767)

# Write the wav file
write('simple-sine.wav', sps, carrier_ints)

plt.ylim([-1, 1])
plt.xlim([0, 1000])
plt.plot(carrier)
plt.show()