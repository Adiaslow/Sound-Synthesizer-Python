import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time
import matplotlib.pyplot as plt


sps = 44100 # samples per second
duration_s = 1.0 # length of signal

scope_scale = 0.5 # y axis of oscilloscope / 2
scope_length_ms = 200 # x axis of oscilloscope in miliseconds

spec_min_hz = 0 # y axis of the spectrogram minimum value
spec_max_hz = 10000 # y axis of the spectrogram maximum value

samples_t = np.arange(sps * duration_s) # broadcast array of samples
print('Number of samples: ' + str(len(samples_t)))

# Osc values
master_amp = 0.2

# Osc 1
freq1 = 440.0 # frequency of carrier wave
oct_shift1 = 1
amp1 = 0.2 # amplitude of carrier wave
v_offset1 = 0.0 # vertical offset of carrier wave
p_shift1 = 0.0 # horizontal offset of carrier wave

mod1_type = 0 # 0 = none, 1 = manual, 2 = square, 3 = harmonic series, 4 = mandelbrot

# Osc 1 Manual Modulation Values
mod1a_amp = 1.0
mod1a_freq = 220.0
mod1b_amp = 1.0
mod1b_freq = 440.0
mod1c_amp = 1.0
mod1c_freq = 880.0

mod1_values = []
mod1_values.append(mod1a_amp)
mod1_values.append(mod1a_freq)
mod1_values.append(mod1b_amp)
mod1_values.append(mod1b_freq)
mod1_values.append(mod1c_amp)
mod1_values.append(mod1c_freq)

# Fourier series
iterations1 = 5


# Osc 1
def osc1(samples_t, freq, amp, v_offset, p_shift, mod_type, mod1_values, iterations1, oct_shift):
    
    if (mod_type == 0): # sine wave
        osc1_signal = amp * np.sin(2 * np.pi * freq * (samples_t + p_shift) / sps) + v_offset
    
    if (mod_type == 1): # sine with manual modulation
        carrier = 2 * np.pi * freq * (samples_t + p_shift) / sps
        
        mod1 = mod1_values[0] * np.sin(2 * np.pi * samples_t * mod1_values[1] / sps)
        mod2 = mod1_values[2] * np.sin(2 * np.pi * samples_t * mod1_values[3] / sps)
        mod3 = mod1_values[4] * np.sin(2 * np.pi * samples_t * mod1_values[5] / sps)
        
        modded_signal = amp1 * np.sin(carrier + mod1 + mod2 + mod3)
        osc1_signal = modded_signal
    
    if (mod_type == 2): # square wave
        osc1_signal = amp * np.sign(np.sin(2 * np.pi * freq * (samples_t + p_shift) / sps) + v_offset)
    
    if (mod_type == 3): # harmonic series
        
        iterations1 *= 2
        
        carrier = np.sin(2 * np.pi * freq * (samples_t + p_shift) / sps) + v_offset # carrier wave
        
        for n in range(3, iterations1 + 2, 2): # finite series loop
            
            temp = (1 / n) * np.sin(2 * n * np.pi * freq1 * (samples_t / sps))
            
            carrier += temp
            
        four_over_pi = amp1 * (4 / np.pi) * carrier # four over pi
        
        osc1_signal = four_over_pi # osc output
        
    if (mod_type == 4):
        
        x, X = -2, 1
        y, Y = -1, 1
        
        delta = 0.004 * (freq / oct_shift / 100)
        
        mandelform = []
        
        re, im = np.mgrid[x:X:delta, y:Y:delta]
        c = (re + 1j*im).reshape(im.shape[0], -1).T
        
        z = np.zeros_like(c)
        escape = np.zeros_like(np.absolute(c))
        for i in range(10):
            z = z * z + c
            idx = (np.absolute(z) > 4) & (escape == 0)
            escape[idx] = 2 * i * np.pi * 1000 * (i / sps)
            
        plt.figure(figsize=(20,10))
        plt.imshow(escape, extent=(x,X,y,Y))
        
        # escape.reshape([escape.size, 1])
        
        for j in escape:
            for k in j:
                mandelform.append(k)
        
        print(len(mandelform))
        file1 = open("mandelform_samples.txt","w")
        file1.write(str(mandelform))
        file1.close()
        
        osc1_signal = amp * np.sin(mandelform * 2)
        
    return osc1_signal


# Output
output = osc1(samples_t,freq1, amp1, v_offset1, p_shift1, mod1_type, mod1_values, iterations1, oct_shift1) # sumation of all oscillators

# Plot
def plots(output, scope_scale, scope_length_ms, sps, spec_min_hz, spec_max_hz):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    fig.suptitle("Signal Analysis", y=1.04)
    
    ax1.plot(output)
    ax1.set_title("Oscilloscope")
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Amplitude (linear)')
    ax1.set_xlim([0,scope_length_ms])
    ax1.set_ylim([-scope_scale , scope_scale])
    
    ax2.specgram(output,Fs = sps, NFFT = 1024, scale_by_freq = True)
    ax2.set_title("Spectrogram")
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Frequency (hz)')
    ax2.set_ylim([spec_min_hz, spec_max_hz])
    
    fig.tight_layout()
    plt.show()

# Play
def play(master_amp, output, sps, duration_s):
    sd.play(master_amp * output, sps)
    time.sleep(duration_s)
    sd.sleep(round(duration_s))

# Write
def write_file(output, sps):
    output_integers = np.int16(output * 32767)
    write('synth3x.wav', sps, output_integers)
    print("Write Successful")

# Execution Time
def execution_time():
    startTime = time.time()
    executionTime = "{:.10f}".format((time.time() - startTime))
    print('Execution time: ' + str(executionTime) + ' seconds')
    
plots(output, scope_scale, scope_length_ms, sps, spec_min_hz, spec_max_hz)
play(master_amp, output, sps, duration_s)
write_file(output, sps)
execution_time()