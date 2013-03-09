import sys
import pickle
from numpy import argmax
from spectrumizer import getFreqSpec
from train_network import class_labels

if len(sys.argv) < 4:
    print "Usage:\nnetwork dataset .wav-file"
    sys.exit(0)

nn = pickle.load(open(sys.argv[1], 'r'))

ds = pickle.load(open(sys.argv[2], 'r'))

freqSpec = getFreqSpec(sys.argv[3], ds.num_freq_bins)

ds.normalizeSpec(freqSpec)

answer = nn.activate(freqSpec)

print answer

print "Is this a \"" + class_labels[argmax(answer)] + "\" sound?"
