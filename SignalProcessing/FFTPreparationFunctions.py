from ImportsFile import *
import numpy
import scipy
import scipy.signal
from SignalProcessing.SpectrogramFilteringFunctions import *

'''
    function mame: stereoToMonoConvert
    output: N/A
    input: N/A
    operation: for every point takes the average of left speaker and the right speaker. 
'''


def stereoToMonoConvert(data):
    # instead of int16 type. takes care of the overflow that occurred.
    data = np.array(data, dtype=numpy.float64)
    return list(map(lambda tup: (tup[0] + tup[1]) / 2, data))


'''
   function name: lowPassFilter
   input: N/A
   output:N/A
   operation: uses butterWorth filter, cutoff frequency of 5kHz, 
'''


def lowPassFilter(data, sampleRate):
    order = 2
    cutOffFrequency = GlobalValues.lowPassFilterFrequency
    nyq = 0.5 * sampleRate  # Nyquist Frequency
    normal_cutoff = cutOffFrequency / nyq

    # Get the filter coefficients
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return scipy.signal.filtfilt(b, a, data)


'''
function name: hammingWindow.
input: data, list of samples from a wav file.
output: result, list of sub-lists, 1024 in length (if possible).
operation: divides the data into 1024 sublist, multiplies with the window function, return the result in a list, takes 
care of the reminders.

'''


def hammingWindow(data):
    windowSize = GlobalValues.hammingWindowSize
    window = np.hamming(windowSize)
    length = len(data)
    subLists = [data[i: i + windowSize] for i in range(0, length - length % windowSize, windowSize)]
    return list(map(lambda subList: [subList[i] * window[i] for i in range(len(subList))], subLists))


'''
function name: 
downSample input: 
N/A output: N/A 
operation: for every 4 sample points we take the average of them, reducing our sample rate to 10.025kHz, a quarter of the original sampling frequency.
takes care of reminders.
'''


def downSample(data):
    length = len(data)
    temp = list(map(lambda subList: sum(subList) / 4, [data[i:i + 4] for i in range(0, (length - length % 4), 4)]))

    if not length % 4 == 0: temp.append(sum(data[-(length % 4):]) / (length % 4))

    return temp


"""
function name: prepareForSpectrogram.
input: sampleRate - the sampling rate of the input data. data - the audio file from wavfile.read. a numpy array.
output: a tuple - sampleRate, data. sample rate is the input sample rate divided by 4 (after the down sampling). data is 
the processed data.
operation: checks the data to be a mono or a stereo file. if it's a mono file it passes the data through the stereoToMonoConvert function. otherwise 
continues as usual with the low pass filter and the down sampling.
"""


def prepareForSpectrogram(sampleRate, data):
    if len(data.shape) == 2:
        print('preparing stereo file...')
        data = stereoToMonoConvert(data)
    else:
        print('preparing mono file...')

    data = lowPassFilter(data, sampleRate)
    data = downSample(data)
    sampleRate /= 4
    return sampleRate, data
