import wave
import sys
import cPickle
import struct
from numpy import argmax, array, zeros, average
from spectrumizer import getFreqSpecFromFile
from train import class_labels

def getSamples(fp, start=0, end=0):
    sample_rate = fp.getframerate()
    num_frames = fp.getnframes() if end == 0 else end-start
    num_channels = fp.getnchannels()
    sample_width = fp.getsampwidth()
    total_samples = num_frames * num_channels
    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")
    fp.setpos(start)
    sample_data = fp.readframes(num_frames)
    samples = struct.unpack(fmt, sample_data)
    channels = array([zeros(num_frames) for channel in range(num_channels)])

    for index, value in enumerate(samples):
        channel = index % num_channels
        frame = index / num_channels
        channels[channel][frame] = value

    mono_signal = average(channels, axis=0)
    return mono_signal

def RMS(samples):
    rms = pow(sum([pow(float(x), 2) for x in samples])/len(samples), 0.5)
    return rms
    # Python is cool

try:
    nn = cPickle.load(open(sys.argv[1], 'r'))
    ds = cPickle.load(open(sys.argv[2], 'r'))
    sound_file = sys.argv[3]
except IndexError:
    sys.stderr.write("Args:\nnetwork dataset sound_file\n")
    sys.exit()

sound_clip_size = 0.1 # in seconds
sound_clip_incr = 0.02 # in seconds
bests = [(None, None)] * len(class_labels)
fft_length = ds.num_freq_bins*2

fp = wave.open(sound_file, 'r')
frame_rate = fp.getframerate()
sound_clip_frames = int(sound_clip_size * frame_rate)
incr_frames = int(sound_clip_incr * frame_rate)
num_frames = fp.getnframes()
total_rms = RMS(getSamples(fp))
for clip in range(0, num_frames-sound_clip_frames, incr_frames):
    rms = RMS(getSamples(fp, clip, clip+sound_clip_frames))
    if rms/total_rms < 0.2:
        continue
    spec, freqs = getFreqSpecFromFile(fp, fft_length, clip, clip+sound_clip_frames)
    ds.normalizeSpec(spec)
    c = nn.activate(spec)
    for i in range(len(bests)):
        if bests[i][0] is None or c[i] > bests[i][0]:
            bests[i] = c[i], clip

nchannels = fp.getnchannels()
sampwidth = fp.getsampwidth()
framerate = fp.getframerate()
nframes = sound_clip_frames
comptype = fp.getcomptype()
compname = fp.getcompname()

for i in range(len(bests)):
    if bests[i][0] is not None:
        fp.setpos(bests[i][1])
        best_file = wave.open(class_labels[i]+'_best.wav', 'w')
        best_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        best_file.writeframes(fp.readframes(sound_clip_frames))
        best_file.close()
fp.close()
