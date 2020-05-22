from DatabaseItems.Song import Song
from DatabaseItems.Recording import Recording
from GeneralFunctions import *
import matplotlib.pyplot as plt

ss = Song('C:\PythonProject\Songs\AdventureOfALifetime045200S.wav', 'test')
ss.createConstellationMap()

sm = Recording()
sm.createConstellationMap()

xs, ys = createLists(ss.timeFrequencyPoints)
xm, ym = createLists(sm.timeFrequencyPoints)

print(len(ss.timeFrequencyPoints))
print(len(sm.timeFrequencyPoints))
intersectionPoints = set(ss.timeFrequencyPoints).intersection(set(sm.timeFrequencyPoints))
print(len(intersectionPoints))
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(xm, ym, 'bx')
plt.plot(xs, ys, 'kx')

plt.subplot(2, 1, 2)
x, y = createLists(intersectionPoints)
plt.plot(x, y, 'rx')
plt.show()
