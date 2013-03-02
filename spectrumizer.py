import scipy
import sys
import scipy.fftpack
import pylab
import wave
import struct
from numpy import hamming, zeros, array, arange, log10
from scipy import pi
from scikits.audiolab import wavread

fp = wave.open(sys.argv[1],"r")
sample_rate = fp.getframerate()
num_frames = fp.getnframes()
num_channels = fp.getnchannels()
sample_width = fp.getsampwidth()
total_samples = num_frames * num_channels

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

mono_signal = array([frame.mean() for frame in channels.transpose()]).transpose()


FFT = 10*log10(abs(scipy.fft(mono_signal)))
freqs = scipy.fftpack.fftfreq(len(mono_signal), d=1.0/float(sample_rate))
pylab.plot(freqs[:len(freqs)/2], FFT[:len(FFT)/2],'x')
pylab.show()
