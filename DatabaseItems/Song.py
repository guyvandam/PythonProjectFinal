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

    """
       function name: initializeAll.
       input: N/A
       output: N/A
       operation: initializes the timeFrequencyPoints, targetZones, anchorPointTargetZoneDict, addressCoupleDict 
       variables. 
    """

    def initializeAll(self):

        # self.timeFrequencyPoints = [(1, 10), (1, 20), (1, 30), (2, 10), (3, 10), (3, 20), (3, 30), (4, 20), (4, 30),
        #                             (5, 20), (6, 10)]

        self.createConstellationMap()
        self.targetZones = createTargetZones(self.timeFrequencyPoints)
        self.anchorPointTargetZoneDict = createAnchorPoints(self.timeFrequencyPoints, self.targetZones)
        self.createAddresses()

    """
        function name: createConstellationMap.
        input: N/A
        output: N/A
        operation: initializes the timeFrequencyPoints variable. it reads the wave file associated with the song 
        instance and prepares the data for the fft. 
    """

    def createConstellationMap(self):
        sampleRate, data = wavefile.read(self.path)
        sampleRate, data = prepareForSpectrogram(sampleRate, data)
        # f, t, Sxx = createSpectrogram(sampleRate, data)
        # self.timeFrequencyPoints, r = filterSpectrogramByRegions(Sxx, f, t, GlobalValues.regionCoefficientD)
        self.timeFrequencyPoints = createFilteredSpectrogramPoints(sampleRate, data)

    """
        function name: createAddresses 
        input: N/A 
        output: N/A 
        operation: initializes the addressAnchorTimeDict, 
        for every point in a target zone, calculates the address according to the anchor point. rounds the number to 3 
        decimal points and saves the result as a String for storage in the database.    
    """

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


if __name__ == '__main__':
    s = Song('C:\PythonProject\Songs\LoseYourself045100S.wav', 'test')
    s.initializeAll()
    print(s.addressCoupleDict)

    # '''
    #     function name: createTargetZone
    #     input: N/A
    #     output: N/A
    #     operation: initializes the 'targetZones' variable.
    #     '''
    #
    # def createTargetZones(self):
    #     self.targetZones = createTargetZones(self.timeFrequencyPoints)

    # '''
    # input: N/A
    # output: list of (couple,address) couples
    # operation: for each target zone, updates the "anchor_targetZoneDict" with a new key - the anchor point and its value
    # the target zone.
    # '''
    #
    # def addressesCreate(self):
    #     self.createAnchorPoints()
    #
    #     for anchorPoint, targetZone in self.anchorPointTargetZoneDict.items():
    #         for p in targetZone:
    #             self.addressCouplesList.append(
    #                 ((anchorPoint[0], self.songID), (anchorPoint[1], p[1], p[0] - anchorPoint[0])))
    #
    #     return self.addressCouplesList
