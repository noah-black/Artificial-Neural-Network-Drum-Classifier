import os
import sys
import scipy
import scipy.fftpack
import pylab
import wave
import struct
from numpy import hamming, zeros, array, arange, log10, average
from scipy import pi
from scikits.audiolab import wavread

def RMS(samples):
    rms = pow(sum([pow(float(x), 2) for x in samples])/len(samples), 0.5)
    return rms

def getAverageOfSquaredDerivative(samples):
    s2 = [pow(sample, 2) for sample in samples]
    s2Prime = []
    prev = s2[0]
    for s in s2[1:]:
        s2Prime.append(s-prev)
        prev = s
    return average(s2Prime)

def getFreqSpec(filename, fft_length, cursorL=0, cursorR=0):
    fp = wave.open(filename, 'r')
    freqspec, freqs = getFreqSpecFromFile(fp, fft_length, cursorL, cursorR)
    fp.close()
    return freqspec, freqs

def getFreqSpecFromFile(fp, fft_length, cursorL=0, cursorR=0):
    sample_rate = fp.getframerate()
    num_frames = fp.getnframes() if cursorR == 0 else cursorR-cursorL
    num_channels = fp.getnchannels()
    sample_width = fp.getsampwidth()
    total_samples = num_frames * num_channels
    num_fft = num_frames / fft_length

    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")
    fp.setpos(cursorL)
    sample_data = fp.readframes(num_frames)
    samples = struct.unpack(fmt, sample_data)
    del sample_data

    channels = array([zeros(num_frames) for channel in range(num_channels)])

    for index, value in enumerate(samples):
        channel = index % num_channels
        frame = index / num_channels
        channels[channel][frame] = value

    mono_signal = average(channels, axis=0)

    s2pavg = getAverageOfSquaredDerivative(mono_signal)

    mono_signal.resize(num_fft, fft_length)

    mono_signal = mono_signal * hamming(fft_length)

    FFT = map(lambda x: map(lambda y: 10*log10(y) if y != 0 else y, x), abs(scipy.fft(mono_signal)))

    freqs = scipy.fftpack.fftfreq(fft_length, d=1.0/float(sample_rate))

    if(num_channels > 1):
        FFT = average(FFT, axis=0)
    else:
        FFT = FFT[0]
    FFT = list(FFT[:len(FFT)/2])
    #FFT.append(s2pavg)
    return FFT, freqs[:len(freqs)/2]

def plotFreqSpec(FFT, freqs):
    pylab.plot(freqs, FFT,'x')
    pylab.show()

def getSpecs(path, num_freq_bins):
    specs = []
    for filename in os.listdir(path):
        freqspec, freqs = getFreqSpec(path+filename, num_freq_bins*2)
        specs.append(freqspec)
    return specs
