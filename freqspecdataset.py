import numpy

class FreqSpecDataset():
    def __init__(self, specs, num_freq_bins):
        self.specs = specs
        self.num_freq_bins = num_freq_bins
        self.normalize(self.specs)

    def normalizeSpec(self, spec):
        for i in range(len(spec)):
            spec[i] = (spec[i] - self.mins[i])/(self.maxes[i]-self.mins[i])
    
    def normalize(self, specs):
        allSpecs = []
        for sound in specs:
            allSpecs += specs[sound]
        allSpecs = numpy.array(allSpecs)
        self.maxes = numpy.max(allSpecs, axis=0)
        self.mins = numpy.min(allSpecs, axis=0)
        for sound in specs:
            for spec in specs[sound]:
                self.normalizeSpec(spec)


