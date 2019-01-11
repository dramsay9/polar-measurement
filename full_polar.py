from pythonAudioMeasurements import audioMeasure
from pythonAudioMeasurements.pyStep import Stepper
from pythonAudioMeasurements.polarPlot import polarPlot
from pyfirmata import Arduino, util
import time

port = "/dev/cu.usbmodem1421"
uno = Arduino(port)

motor = Stepper(uno, [3,4,5,6])
#motor.turn(360)
#
#while True:
#   motor.turn(360)
#   time.sleep(0.5)

plot = polarPlot(makeMotor=True, board=port, testSignalRepetitions=100)
plot.makePlot(motor = True, numMeasurements=36, measurementFrequencies={250,500, 1000, 2000, 4000, 8000, 16000})
