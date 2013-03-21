import os
import sys
from spectrumizer import getSpecs
from freqspecdataset import FreqSpecDataset
import cPickle

try:
    num_freq_bins = int(sys.argv[1])
    if num_freq_bins < 1:
        raise ValueError
except IndexError:
    sys.stderr.write("Must provide number of frequency bins\n")
    sys.exit()
except ValueError:
    sys.stderr.write("Must provide a positive number of frequency bins\n")
    sys.exit()

specs = { 
    'snares'    : getSpecs('training_drums/snares/', num_freq_bins), 
    'hats'      : getSpecs('training_drums/hats/', num_freq_bins), 
    'kicks'     : getSpecs('training_drums/kicks/', num_freq_bins) 
}

dataset = FreqSpecDataset(specs, num_freq_bins)

cPickle.dump(dataset, open('datasets/dataset'+str(num_freq_bins), 'wb'))
