import sys
from spectrumizer import getFreqSpec, plotFreqSpec

spec, freqs = getFreqSpec(sys.argv[1], 1024)
plotFreqSpec(spec, freqs)
