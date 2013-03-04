import os
import sys
from spectrumizer import getFreqSpec
import cPickle
import numpy
from numpy import array

num_freq_bins = int(sys.argv[1])

def getSpecs(path):
    specs = []
    for filename in os.listdir(path):
        FFT, freqspec = getFreqSpec(path+filename, num_freq_bins)
        specs.append(FFT)
    return specs

def normalize(specs):
    allSpecs = []
    for sound in specs:
        allSpecs += specs[sound]
    allSpecs = array(allSpecs)
    maxes = numpy.max(allSpecs, axis=0)
    mins = numpy.min(allSpecs, axis=0)
    for sound in specs:
        for spec in specs[sound]:
            for i in range(num_freq_bins):
                spec[i] = (spec[i] - mins[i])/(maxes[i]-mins[i])

specs = { 'snares' : getSpecs('sounds/snares/'), 'hats' : getSpecs('sounds/hats/'), 'kicks' : getSpecs('sounds/kicks/') }

normalize(specs)

cPickle.dump(specs, open('freqspecs'+str(num_freq_bins), 'wb'))
