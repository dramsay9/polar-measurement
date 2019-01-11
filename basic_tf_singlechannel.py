import cPickle as pickle
from pythonAudioMeasurements.audioMeasure import audioMeasure
audioMeas = audioMeasure(Fs=44100)
audioMeas.pinkNoiseLoop(samples=8192, repetitions=100)
audioMeas.testAllChannels()
audioMeas.calcTF()

audioMeas.plotFreqResp() #plot freq response of each channel
audioMeas.plotImpulseResp() #plot IR of each channel

audioSamp = audioMeas.tf[0]
audioSamp.toDb()

pickle.dump(audioSamp, open('measurement_mic_baseline.pkl', 'wb'))
