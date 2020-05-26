import GlobalValues
from ImportsFile import *
import scipy.fftpack as fftpk
from pylab import *

# frequencies bands ranges.
RANGE = [102.315, 210.015, 425.415, 856.215, 1717.815, 5508.855]
# the bands values.
bandsValue = [9, 19, 39, 79, 159, 511]
windowSize = 1024
sampleRate = 11025

frequencies = fftpk.fftfreq(windowSize, d=(1.0 / sampleRate))
frequencies = frequencies[0:len(frequencies) // 2]

"""
function name: updateRange.
input: N/A
output: N/A
operation: update the frequency RANGE variable. 
"""


def updateRange():
    global RANGE
    RANGE = list(map(getNthBin, bandsValue))


"""
function name: getNthBin.
input: n, a natural number. 
output: returns the nth bin upper limit with a bin size of 10.77Hz.
operation: a recursive function. the first bin is (0,binSize/2) and the following bins are the intervals where the bin 
Size is added to a and b [(a,b)]. 
"""


def getNthBin(n):
    binSize = 10.77
    if 0 == n:
        return binSize / 2
    else:
        return getNthBin(n - 1) + binSize


"""
function name: pointIntoBand.
input: bands - a dictionary of lists. (key - the number of band, value - a list of points with frequency in that band)
        point - a frequency-amplitude point.
output: N/A
operation: goes with a loop until the point is no longer in that band and stops.
"""


def pointIntoBand(bands, point):
    i = 0
    length = len(bands)
    while RANGE[i] <= frequencies[point[0]] and i < length - 1:
        i += 1
    bands[i].append(point)


"""
function name: FFTPointsIntoBands.
input: frequencyAmplitudePoints - a list of the frequency-amplitude points returned by the fft.
output: bands - a dictionary (key - the number of band, value - a list of points with frequency in that band). 
operation: loops through the input list and calls the pointIntoBand function.
"""


def FFTPointsIntoBands(frequencyAmplitudePoints):
    bands = {i: [] for i in range(6)}
    for p in frequencyAmplitudePoints:
        pointIntoBand(bands, p)

    return bands


'''
function name: maxOfBand
input: the dictionary of points after the distribution to bands.
output: the same dictionary, with only the bigger amplitude points left. the strongest point of each band.
operation: uses the max function with the key set to the amplitude (the second value of the pair)
'''


def maxOfBand(bands):
    for key in bands:
        try:
            bands[key] = max(bands[key], key=lambda x: x[1])  # amplitude.
        except:
            print(str(key) + "is empty")
    return bands


'''
function name: averageValueOfBins
input: the dictionary of strongest point of each band
output: the average value of the frequency of these bins
operation: average of all the value in the dictionary.
'''


def averageValueOfBins(bands):
    try:
        return sum([v[1] for v in bands.values()]) / len(bands)  # amplitude.
    except Exception:
        print("error in summing the values in averageValueOfBins")
        exit(1)


'''
function name: passAboveTheMean.
input: the bans dictionary as seen before.
output: a list of the points whose amplitude is above the averageValue of the max of each band, multiplied by a 
coefficient.
operation: self explanatory.
'''


def passAboveTheMean(bands):
    averageValue = averageValueOfBins(bands)
    meanCoefficient = GlobalValues.meanCoefficient

    return [v for v in bands.values() if v[1] >= averageValue * meanCoefficient]


'''
function name: filterFFT.
input: the time-frequency points were getting from the fft.
output: the peak points of that fft.
operation: puts the points in the bands, keeps only the max of these bands and pass the points that are above the mean..
'''


def filterFFT(frequencyAmplitudePoints):
    bands = FFTPointsIntoBands(frequencyAmplitudePoints)
    bands = maxOfBand(bands)

    return passAboveTheMean(bands)
