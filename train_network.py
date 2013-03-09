import sys
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import TanhLayer, LinearLayer, SoftmaxLayer, SigmoidLayer
from scipy import diag, arange, meshgrid, where
from freqspecdataset import FreqSpecDataset
import cPickle
import time

class_labels=['snare', 'hat', 'kick']

if __name__=="__main__":
    num_epochs = int(sys.argv[1])
    filename = sys.argv[2]
    momentum = 0.2
    weightdecay = 0.0001
    
    dataset = cPickle.load(open(filename, 'rb'))
    
    num_freq_bins = len(dataset.specs['snares'][0])
    
    ds = ClassificationDataSet(num_freq_bins, nb_classes=3)
    
    for spec in dataset.specs['snares']:
        ds.addSample(spec, [0])
    for spec in dataset.specs['hats']:
        ds.addSample(spec, [1])
    for spec in dataset.specs['kicks']:
        ds.addSample(spec, [2])
    
    tstdata, trndata = ds.splitWithProportion( 0.05 )
    
    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )
    
    #fnn = buildNetwork(trndata.indim, (num_freq_bins/2)-1, trndata.outdim, hiddenclass=SigmoidLayer, outclass=SoftmaxLayer )
    fnn = buildNetwork(trndata.indim, (num_freq_bins/2)-1, trndata.outdim, outclass=SoftmaxLayer )
    
    trainer = BackpropTrainer(fnn, dataset=trndata, momentum=momentum, verbose=True, weightdecay=weightdecay)
    
    ticks = arange(-3.,6.,0.2)
    X, Y = meshgrid(ticks, ticks)
    # need column vectors in dataset, not arrays
    griddata = ClassificationDataSet(2,1, nb_classes=3)
    for i in xrange(X.size):
        griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
    griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy
    
    for i in range(1):
        trainer.trainEpochs(num_epochs)
    
        trnresult = percentError(trainer.testOnClassData(), trndata['class'])
        tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
    
        print trnresult
        print tstresult
    
        print "epoch: %4d" % trainer.totalepochs, \
              "  train error: %5.2f%%" % trnresult, \
              "  test error: %5.2f%%" % tstresult
    
    cPickle.dump(fnn , open('network'+str(num_freq_bins), 'wb'))
