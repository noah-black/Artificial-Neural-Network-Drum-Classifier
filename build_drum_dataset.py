import os
import sys
from spectrumizer import getSpecs
from freqspecdataset import FreqSpecDataset
import cPickle

num_freq_bins = int(sys.argv[1])

specs = { 
    'snares'    : getSpecs('sounds/snares/', num_freq_bins), 
    'hats'      : getSpecs('sounds/hats/', num_freq_bins), 
    'kicks'     : getSpecs('sounds/kicks/', num_freq_bins) 
}

dataset = FreqSpecDataset(specs, num_freq_bins)


cPickle.dump(dataset, open('drum_datasets/dataset'+str(num_freq_bins), 'wb'))
