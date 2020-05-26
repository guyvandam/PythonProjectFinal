from ImportsFile import *
import scipy
import scipy.signal
from pylab import *
from GeneralFunctions import *

'''
function name: FFT.
input: data, sampleRate.
output: a tuple, (frequency, amplitudes)
operation: uses the scipy built-in function, cuts the result in half because of the symmetry, takes care of the
amplitude units.
'''


def FFT(data):
    amplitude = abs(scipy.fft.fft(data))
    amplitude = 2 * amplitude[0:len(amplitude) // 2]
    amplitude = amplitude / len(data)

    return amplitude


'''
function name: createFilteredSpectrogramPoints.
input: data - the audio data after been pass through the preparation stages. 
output: a list of time - frequency PEAK points. (the peaks are chosen according to their amplitude and by the filtering algorithm.
operation: calculates the fft for every 1024 points (after going through the hamming window function) in the input data. and passes the result 
through the filtering algorithm. 
'''


def createFilteredSpectrogramPoints(data):
    spectrogramPoints = []
    result = hammingWindow(data)

    for i in range(len(result)):
        amp = FFT(result[i])
        frequencyAmplitudePoints = createPoints([*range(0, 512)], amp)
        filteredPoints = filterFFT(frequencyAmplitudePoints)
        for f in filteredPoints:
            spectrogramPoints.append((i / 10, round(f[0], 3)))

        spectrogramPoints = sorted(spectrogramPoints, key=lambda x: x[0])  # filter the points by time.
    return spectrogramPoints
