__Artificial Neural Network Drum Classifier__
=============================================
*by Noah Black, for CS 485*

REQUIRED LIBRARIES:
* PyBrain (ANN stuff)
* Scipy (FFT stuff)
* Numpy (convenient matrix/array methods)
* Pylab (for plotting spectrum)

__TO PREPARE A NETWORK__:

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


__TO USE A NETWORK__:

You may use the network to classify audio files using 'classify.py'. You need to provide the network *and* the dataset. This is because the dataset knows the number of frequency bands, and the network doesn't. I should just find a way of embedding frequency band number into the serialized network (subclassing PyBrain's network class, or whatever).

    Usage:
        python classify.py [network] [dataset] [.wav-file] 

__TO EXTRACT DRUM SOUNDS FROM RECORDING__:
Use the extract.py script. This puts the files 'hat\_best.wav', 'snare\_best.wav', 'kick\_best.wav' in the current directory.

    Usage:
        python extract.py [network] [dataset] [.wav-file] 

__TO DISPLAY A PLOT THE FREQUENCY SPECTRUM OF AN AUDIO FILE__:

Use plot.py
    Usage: 
        python plot.py [sound file] [number of frequency bands]
