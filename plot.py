import sys
import cPickle
from spectrumizer import getFreqSpec, plotFreqSpec

try:
    filename = sys.argv[1]
    fft_length = int(sys.argv[2])
except IndexError:
    sys.stderr.write('Usage: sound file, fft length\n')
    sys.exit(1)


spec, freqs = getFreqSpec(filename, fft_length)
plotFreqSpec(spec, freqs)
