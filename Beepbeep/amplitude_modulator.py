# Import
import numpy as np
from scipy.io.wavfile import write

# Properties of the wav
sps = 44100
carrier_hz = 440.0
modulator_hz = 0.25
ac = 1.0
ka = 0.25
duration_s = 10.0

# Calculate the sine wive
t_samples = np.arange(sps * duration_s)
carrier = np.sin(2 * np.pi * carrier_hz * t_samples / sps)


# Modulate the carrier
modulator = np.sin(2 * np.pi * modulator_hz * t_samples / sps)
envelope = ac * (1.0 + ka * modulator)
modulated = envelope * carrier

# Write the wav file
modulated *= 0.3
modulated_ints = np.int16(modulated * 32767)
write('amplitude_modulated.wav', sps, modulated_ints)