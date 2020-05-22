from scipy.io.wavfile import *

from SignalProcessing.SpectrogramFilteringFunctions import *

path = 'C:\PythonProject\Songs\LoseYourself045100MS.wav'
sampleRate, data = wavefile.read(path)
left = list(data[:, 0])
right = list(data[:, 1])
avg = stereoToMonoConvert(data)

plt.figure(figsize=(11, 7))
plt.subplot(3, 1, 1)
plt.plot(avg)
plt.plot(left)

plt.subplot(3, 1, 2)
plt.plot(avg)
plt.plot(right)

plt.subplot(3, 1, 3)
plt.plot(avg)

plt.show()
