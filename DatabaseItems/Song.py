from ImportsFile import *


decimalPoints = GlobalValues.decimalPoints


class Song:

    def __init__(self, path, songID):
        self.path = path
        self.songID = songID

        self.timeFrequencyPoints = []

        self.targetZones = []

        self.anchorPointTargetZoneDict = {}  # key - anchor point, value - target zone

        self.addressCouplesList = []

        self.addressCoupleDict = {}

    def initializeAll(self):

        # self.timeFrequencyPoints = [(1, 10), (1, 20), (1, 30), (2, 10), (3, 10), (3, 20), (3, 30), (4, 20), (4, 30),
        #                             (5, 20), (6, 10)]

        self.createConstellationMap()
        self.targetZones = createTargetZones(self.timeFrequencyPoints)
        self.createAnchorPoints()
        self.createAddresses()

    '''
    function name: createTimeFrequencyPoints.
    input:N/A
    output: N/A
    operation: initializes the 'timeFrequencyPoints' variable.
    '''

    # def createTimeFrequencyPoints(self):
    #     sampleRate, data = scipy.io.wavfile.read(self.path)
    #     self.timeFrequencyPoints = createFilteredSpectrogram(sampleRate, data)

    def createConstellationMap(self):
        sampleRate, data = wavefile.read(self.path)
        sampleRate, data = prepareForSpectrogram(sampleRate, data)
        f, t, Sxx = createSpectrogram(sampleRate, data)
        self.timeFrequencyPoints, r = filterSpectrogramByRegions(Sxx, f, t, GlobalValues.regionCoefficientD)
        self.timeFrequencyPoints = createFilteredSpectrogram(sampleRate,data)

    '''
        function name: createTargetZone
        input: N/A
        output: N/A
        operation: initializes the 'targetZones' variable.
        '''

    def createTargetZones(self):
        self.targetZones = createTargetZones(self.timeFrequencyPoints)

    '''
    input: N/A
    output: list of (couple,address) couples  
    operation: for each target zone, updates the "anchor_targetZoneDict" with a new key - the anchor point and its value
    the target zone.
    '''

    def addressesCreate(self):
        self.createAnchorPoints()

        for anchorPoint, targetZone in self.anchorPointTargetZoneDict.items():
            for p in targetZone:
                self.addressCouplesList.append(
                    ((anchorPoint[0], self.songID), (anchorPoint[1], p[1], p[0] - anchorPoint[0])))

        return self.addressCouplesList

    def createAddresses(self):
        for anchorPoint, targetZone in self.anchorPointTargetZoneDict.items():
            couple = (round(anchorPoint[0], decimalPoints), self.songID)
            for p in targetZone:
                tempAddress = str(int(round(anchorPoint[1], decimalPoints) * 1000)) + ',' + str(
                    int(round(p[1], decimalPoints) * 1000)) + ',' + str(
                    int(round(p[0] - anchorPoint[0], decimalPoints) * 1000))

            if tempAddress in self.addressCoupleDict:
                self.addressCoupleDict[tempAddress].append(couple)
            else:
                self.addressCoupleDict[tempAddress] = [couple]

    '''
    function name: createAnchorPoints
    input: N/A
    output:N/A
    operation: initializes the 'anchorPointTargetZoneDict' variable.
    '''

    def createAnchorPoints(self):
        self.anchorPointTargetZoneDict = {self.timeFrequencyPoints[i - 3]: self.targetZones[i] for i in
                                          range(3, len(self.targetZones))}

    def plotConstellationMap(self):
        x, y = createLists(self.timeFrequencyPoints)
        plt.plot(x, y, 'kx')
        plt.ylim(0, 5000)
        plt.grid()
        plt.show()


if __name__ == '__main__':
    s = Song('C:\PythonProject\Songs\LoseYourself045100S.wav', 'test')
    s.initializeAll()
    print(s.addressCoupleDict)

    # r = Song("C:\PythonProject\Songs\LoseYourself045100R3.wav", 'recording')
    # r.initializeAll()
    #
    # xs,ys = createLists(s.timeFrequencyPoints)
    # xr,yr = createLists(r.timeFrequencyPoints)
    #
    # plot(xs,ys,'kx')
    # plot()
