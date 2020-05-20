"""

Sample optimization using both the pythonAudioMeasurements and
pyAudioFilter library

author: Tony Terrasa

"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from pythonAudioMeasurements.polarData import polarData
from pythonAudioMeasurements.microphone import Microphone
from pythonAudioMeasurements.microphoneArray import MicrophoneArray
from pyAudioFilter.polar_optimizer import PolarOptimizer


# use to help with GPU tensorflow warnings of you
# have not configured or don't have a GPU
tf.config.set_visible_devices([], 'GPU')


# ------------------------------------------------------------------------------------------
# SET-UP
# ------------------------------------------------------------------------------------------

# load in a microphone
filename = "/home/terrasa/UROP/polar-measurement/data/19_Jan15_fixedpkls/spv1840.pkl" 
pd = polarData.fromPkl(filename)

# set specific locations for the mics
locations = [(0,0), (100,200), (-100, 200), (-100,-200), (100,-200)]

# alternate method of generating mics randomly in a box of a specified width
num_mics = 20
box_width = 600 # mm
locations = box_width*np.random.rand(num_mics,2) # comment to use set microphone locations

# create a microphone array
mic_array =  MicrophoneArray([Microphone(pd, loc) for loc in locations])

# look at where the microphones visualize array geometry
mic_array.visualize()

# convert to tensor-flow representations
angles, freqs, mic_responses = mic_array.tf_prep()
angles = tf.constant(angles)
freqs = tf.constant(freqs)
mic_responses = [tf.constant(mic) for mic in mic_responses]
fs = tf.constant(44.1e3, dtype=freqs.dtype)

# create a PolarOptimizer object
po = PolarOptimizer(angles, freqs, mic_responses, fs=fs, learning_rate=0.01)

# ------------------------------------------------------------------------------------------
# OPTIMIZATION
# ------------------------------------------------------------------------------------------

# set our stop band
stop_band_theta = [45, 135]
target_range_freq = [500, 1000]

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

# plot the losses over epoch
plt.figure(2)
plt.plot(losses)
plt.title("Loss over Epoch. Stop band: theta=(%d,%d), f=(%.2f, %.2f)"%(\
    10,60,500,1000))

# plot the final polarData
pd = po.to_polar_data()
pd.plotFreqs(np.linspace(target_range_freq[0], target_range_freq[1], 5), show=False)

plt.show()