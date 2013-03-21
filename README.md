Artificial Neural Network Drum Classifier
by Noah Black
*For CS 385*

REQUIRED LIBRARIES:
PyBrain (ANN stuff, Scipy (FFT stuff), Numpy (convenient matrix/array methods), Pylab (for plotting spectrum)

_TO PREPARE A NETWORK_:

1. Prepare the training drum sounds
    The training dataset should be in a directory called 'training\_dataset'. Inside of 'training\_drums' there need to be 'snare', 'hat', and 'kick' subdirectories. Inside each of these should be 16-bit wav files.

2. Prepare the dataset
    The sound files are processed into a 'dataset' file by the 'build_dataset.py' script. You must provide the number of frequency bands. The dataset file is saved in ./datasets/dataset<num bands>
    Usage:
        python build_dataset.py [number of frequency bands]

3. Generate and train a network
    Use the 'train.py' script to generate and train a network. The network file is saved in ./networks/network<num bands>
    Usage:
        python train.py [number of training epochs] [dataset file path]


_TO USE A NETWORK_:

You may use the network to classify audio files using 'classify.py'. You need to provide the network *and* the dataset. This is because the dataset knows the number of frequency bands, and the network doesn't. I should just find a way of embedding frequency band number into the serialized network (subclassing PyBrain's network class, or whatever).

    Usage:
        python classify.py [network] [dataset] [.wav-file] 

_TO EXTRACT DRUM SOUNDS FROM RECORDING_:
Use the extract.py script. This puts the files 'hat\_best.wav', 'snare\_best.wav', 'kick\_best.wav' in the current directory.

    Usage:
        python extract.py [network] [dataset] [.wav-file] 

_TO DISPLAY A PLOT THE FREQUENCY SPECTRUM OF AN AUDIO FILE_:

Use plot.py
    Usage: 
        python plot.py [sound file] [number of frequency bands]
