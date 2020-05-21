from ImportsFile import *

'''
    function mame: stereoToMonoConvert
    output: N/A
    input: N/A
    operation: for every point takes the average of left speaker and the right speaker. 
'''


def stereoToMonoConvert(data):
    # saves samples as numpy array:
    """temp = np.empty([0])
     for left, right in self.samples:
         temp = np.append(temp,(left+right)/2)

    self.samples = temp"""

    data = np.array(data, dtype=numpy.float64)  # instead of int16 type.
    return list(map(lambda tup: (tup[0] + tup[1]) / 2, data))


'''
   function name: lowPassFilter
   input: N/A
   output:N/A
   operation: uses butterWorth filter, cutoff frequency of 5kHz, 
'''


def lowPassFilter(data, sampleRate):
    order = 2
    cutOffFrequency = 5000
    nyq = 0.5 * sampleRate  # Nyquist Frequency
    normal_cutoff = cutOffFrequency / nyq

    # Get the filter coefficients
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return scipy.signal.filtfilt(b, a, data)


# low pass filter, than the stereo to mono conversion.
# def lowPassFilter2(data, sampleRate):
#     left = lowPassFilter([l for l, r in data], sampleRate)
#     right = lowPassFilter([r for l, r in data], sampleRate)
#     return [(left[i] + right[i]) / 2 for i in range(len(left))]


'''
function name: hammingWindow.
input: data, list of samples from a wav file.
output: result, list of sub-lists, 1024 in length (if possible).
operation: divides the data into 1024 sublist, multiplies with the window function, return the result in a list, takes 
care of the reminders.

'''


def hammingWindow(data):
    result = []

    windowSize = 1024
    window = np.hamming(windowSize)

    j = 0
    while j + windowSize < len(data):
        result.append([data[j + i] * window[i] for i in range(0, windowSize)])
        j += windowSize

    windowSize = len(data) - j

    result.append([data[j + i] * window[i] for i in range(0, windowSize)])

    return result





'''
function name: 
downSample input: 
N/A output: N/A 
operation: for every 4 sample points we take the average of them, reducing our sample rate to 10.025kHz, 
a quarter of the original sampling frequency. takes care of reminders.
'''


def downSample(data):
    # saves samples as numpy array
    """
    temp = np.empty([0])
    i = 0
    while i < len(self.samples):
        try:
            temp = np.append(temp, (self.samples[i] + self.samples[i + 1] + self.samples[i + 2] + self.samples[i + 3]) / 4)
        except:
            sum = 0
            counter = 0
            while i < len(self.samples):
                sum += self.samples[i]
                counter += 1
                i += 1
            temp = np.append(temp, sum / counter)

        i += 4
    self.samples = temp
    """

    # older approach:
    """ 
    temp = []
    i = 0
    while i < len(data):
        try:
            temp.append((data[i] + data[i + 1] + data[i + 2] + data[i + 3]) / 4)
        except Exception:
            sum = 0
            counter = 0
            while i < len(data):
                sum += data[i]
                counter += 1
                i += 1
            temp.append(sum / counter)

        i += 4
    return temp
    """

    length = len(data)
    temp = list(map(lambda subList: sum(subList) / 4, [data[i:i + 4] for i in range(0, (length - length % 4), 4)]))

    if not length % 4 == 0: temp.append(sum(data[-(length % 4):]) / (length % 4))

    return temp
