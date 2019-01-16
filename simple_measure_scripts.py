#init
import cPickle as pickle
from audioMeasure import audioMeasure
from polarPlot import polarPlot
from pyStep import Stepper
from pyfirmata import Arduino, util
import time
a = audioMeasure(channels=1)
a.aplayer.setVolume(-12)
a.pinkNoiseLoop(8192, 20)
port = "/dev/cu.usbmodem14141"
uno = Arduino(port)
motor = Stepper(uno, [3,4,5,6])



#test a channel and plot
a.testAllChannels()
a.calcTF()
a.plotImpulseResp()
a.plotFreqResp()

#save
asamp = a.tf[0]
asamp.toDb()
pickle.dump(asamp, open('measurement_mic_baseline_011519.pkl', 'wb'))



#turntable
motor.turn(360)
motor.calibrate()

while True:
   motor.turn(360)
   time.sleep(0.5)



#actual polar
plot = polarPlot(usingMotor=motor, board=port, audioMeasure=a)
plot.makePlot(numMeasurements=36, measurementFrequencies={250,500, 1000, 2000, 4000, 8000, 16000})


