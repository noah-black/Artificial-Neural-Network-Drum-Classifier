import scipy
import sys
import scipy.fftpack
import pylab
import wave
import struct
from numpy import hamming, zeros, array, arange, log10, average
from scipy import pi
from scikits.audiolab import wavread

def getFreqSpec(filename, fft_length):
    fp = wave.open(filename ,"r")
    sample_rate = fp.getframerate()
    num_frames = fp.getnframes()
    num_channels = fp.getnchannels()
    sample_width = fp.getsampwidth()
    total_samples = num_frames * num_channels
    num_fft = num_frames / 512

    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    sample_data = fp.readframes(num_frames)
    fp.close()

    samples = struct.unpack(fmt, sample_data)
    del sample_data

    channels = array([zeros(num_frames) for channel in range(num_channels)])

    for index, value in enumerate(samples):
        channel = index % num_channels
        frame = index / num_channels
        channels[channel][frame] = value

    mono_signal = average(channels, axis=0)

    mono_signal.resize(num_fft, fft_length)

    mono_signal = mono_signal * hamming(fft_length)

    FFT = map(lambda x: map(lambda y: 10*log10(y) if y != 0 else y, x), abs(scipy.fft(mono_signal)))

    freqs = scipy.fftpack.fftfreq(fft_length, d=1.0/float(sample_rate))

    if(num_channels > 1):
        FFT = average(FFT, axis=0)
    else:
        FFT = FFT[0]
    return FFT

def plotFreqSpec(FFT, freqs):
    pylab.plot(freqs[:len(freqs)/2], FFT[:len(FFT)/2],'x')
    pylab.show()

def getSpecs(path, num_freq_bins):
    specs = []
    for filename in os.listdir(path):
        freqspec = getFreqSpec(path+filename, num_freq_bins)
        specs.append(freqspec)
    return specs
