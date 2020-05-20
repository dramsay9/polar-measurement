---
title: polar-measurement
author: Tony Terrasa, David Ramsay
---

# polar-measurement

This module contains scripts for taking polar measurements as well as 
well as submodules for creating and manipulating microphone arrays 
and optimizing filters to achieve a desired response in `tensorflow`





# Installation

This package requires python

It is recommended that you use a virtual environment so that it does not
interfere with your local version of Python or `numpy`. From within your 
virual environment and in the `polar-measurement` folder:

```
$ pip3 install -r requirements.txt
```

Next, I recommend that you link the submodules of polar-measurement to 
the `site-packages` directory in your virtual environment or to your 
PYTHONPATH

```
$ ln -s /path_to_polar-measurement/pythonAudioMeasurements /path_to_virtualenv/lib/python3.6/site-packages/
$ ln -s /path_to_polar-measurement/pyAudioFilter /path_to_virtualenv/lib/python3.6/site-packages/
```

You should now be able to use the packages. You can test by running the following without errors

```
$ python3
Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pythonAudioMeasurements.audioSample import audioSample
>>> from pyAudioFilter.polar_optimizer import PolarOptimizer
```


# Usage

There are examples show in the submodule of how to use individual submodules. 
Below is information on how to use them together, namely to optimize filters 
for a microphone array to achieve a stop-band in theta and frequency


First, the necessary imports:

```
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from pythonAudioMeasurements.polarData import polarData
from pythonAudioMeasurements.microphone import Microphone
from pythonAudioMeasurements.microphoneArray import MicrophoneArray
from pyAudioFilter.polar_optimizer import PolarOptimizer
```

Next, we should create a `MicrophoneArray` of the same microphone from
the `data/19_Jan15_fixedpkls` folder. 

Load in the a microphone as a `polarData` object. 

```
filename = "/path_to_polar-measurement/data/19_Jan15_fixedpkls/spv1840.pkl" 
pd = polarData.fromPkl(filename)
```

Now, set locations, create `Microphone` instances and store them in a 
`MicrophoneArray` instance. 

```
# set specific locations for the mics, given as x,y in mm
locations = [(0,0), (100,200), (-100, 200), (-100,-200), (100,-200)]

# create a microphone array
mic_array =  MicrophoneArray([Microphone(pd, loc) for loc in locations])
```

Alternatively, it you would like to randomly generate locations of _many_ 
microphones:

```
num_mics = 20
box_width = 600 # mm
locations = box_width*np.random.rand(num_mics,2) 
```

These instances can now be used to visualize the `Microphone` or 
`MicrophoneArray`. 
- To do: add a way to quickly show the `polarData` response at certain 
frequencies

```
mic_array.visualize() # plots the microphone locations
```

However, these representations need to formated to be used in a `tensorflow` 
model. 

```
# return np.array's
angles, freqs, mic_responses = mic_array.tf_prep()

angles = tf.constant(angles)
freqs = tf.constant(freqs)
mic_responses = [tf.constant(mic) for mic in mic_responses]
fs = tf.constant(44.1e3, dtype=freqs.dtype)

po = PolarOptimizer(angles, freqs, mic_responses, fs=fs, learning_rate=0.01)
```

Now  we set a target angle and frequencies for our stop-band

```
stop_band_theta = [45, 135]
target_range_freq = [500, 1000]
```

And, we are ready to run our optimization

```
losses = []
NUM_EPOCHS = 60

for epoch in range(NUM_EPOCHS):

    # run a step
    po.train(stop_band_theta, target_range_freq, threshold=-20.)
    losses.append(po.current_loss.numpy()) # keep track of the loss over the epochs

    if epoch % 10 == 0:
        pd = po.to_polar_data()
        pd.plotFreqs(np.linspace(target_range_freq[0], target_range_freq[1], 5),\
            title="epoch: %d, loss: %.2f"%(epoch, losses[-1]))

plt.figure(2)
plt.plot(losses)
plt.title("Loss over Epoch. Stop band: theta=(%d,%d), f=(%.2f, %.2f)"%(\
    10,60,500,1000))

pd_final = po.to_polar_data()
pd_final.plotFreqs(np.linspace(target_range_freq[0], target_range_freq[1], 5), show=False)

plt.show()
```

In this case `pd_final` is now a `polarData` representation of the 
resulting microphone array. 

A full version of this script can be found in the `sample_optimization.py`