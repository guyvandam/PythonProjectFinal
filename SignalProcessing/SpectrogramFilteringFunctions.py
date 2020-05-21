from ImportsFile import *

RANGE = [102.315, 210.015, 425.415, 856.215, 1717.815, 5508.855]
bandsValue = [9, 19, 39, 79, 159, 511]
windowSize = 1024
sampleRate = 11025

# frequencies = fftpk.fftfreq(windowSize, d=(1.0 / sampleRate))
# frequencies = frequencies[0:len(frequencies) // 2]


def updateRange():
    global RANGE
    RANGE = list(map(getNthBin, bandsValue))


def getNthBin(n):
    binSize = 10.77
    if 0 == n:
        return binSize / 2
    else:
        return getNthBin(n - 1) + binSize


def pointIntoBand(bands, point):
    i = 0
    length = len(bands)
    while RANGE[i] <= point[0] and i < length - 1:
        i += 1
    bands[i].append(point)


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
this is the step 4, i think it means keeping the bin that are above the average of the 6 max bands. multiplied by a
coefficient
'''


def passAboveTheMean(bands):
    averageValue = averageValueOfBins(bands)
    meanCoefficient = GlobalValues.meanCoefficient

    return [v for v in bands.values() if v[1] >= averageValue * meanCoefficient]


'''
does this for just one fft sample.
'''


def filterFFT(frequencyAmplitudePoints):
    bands = FFTPointsIntoBands(frequencyAmplitudePoints)
    bands = maxOfBand(bands)

    return passAboveTheMean(bands)
