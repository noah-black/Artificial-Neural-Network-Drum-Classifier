import os
import sys
from spectrumizer import getSpecs
from freqspecdataset import FreqSpecDataset
import cPickle

num_freq_bins = int(sys.argv[1])

specs = { 
    'a'         : getSpecs('pitch_sounds/a/', num_freq_bins), 
    'asharp'    : getSpecs('pitch_sounds/asharp/', num_freq_bins), 
    'b'         : getSpecs('pitch_sounds/b/', num_freq_bins) 
    'c'         : getSpecs('pitch_sounds/c/', num_freq_bins), 
    'csharp'    : getSpecs('pitch_sounds/csharp/', num_freq_bins), 
    'd'         : getSpecs('pitch_sounds/d/', num_freq_bins), 
    'dsharp'    : getSpecs('pitch_sounds/dsharp/', num_freq_bins), 
    'e'         : getSpecs('pitch_sounds/e/', num_freq_bins), 
    'f'         : getSpecs('pitch_sounds/f/', num_freq_bins), 
    'fsharp'    : getSpecs('pitch_sounds/fsharp/', num_freq_bins), 
    'g'         : getSpecs('pitch_sounds/g/', num_freq_bins), 
    'gsharp'    : getSpecs('pitch_sounds/gsharp/', num_freq_bins)
}

dataset = FreqSpecDataset(specs, num_freq_bins)

cPickle.dump(dataset, open('pitch_datasets/dataset'+str(num_freq_bins), 'wb'))
