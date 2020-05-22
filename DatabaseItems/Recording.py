from DatabaseItems.Song import Song
from ImportsFile import *

decimalPoints = GlobalValues.decimalPoints
coefficient = GlobalValues.songIdFilterCoefficient


class Recording:
    def __init__(self):
        self.timeFrequencyPoints = []

        self.targetZones = []

        self.anchorPointTargetZoneDict = {}  # key - anchor point, value - target zone

        # self.addressCouplesList = []

        self.addressAnchorTimeDict = {}

        # key - couple, value - the number of time it appears in the recording address.
        self.songIdTable = {}

        # key - songId, value - the number of time is part of a key in the songIdTable
        self.songIdNumOfKeysTable = {}
        # key - songId, value - a list of deltas of the anchor time for each songId.
        self.songIdDeltaDict = {}

    """
    function name: initializeAll.
    input: N/A
    output: N/A
    operation: initializes the timeFrequencyPoints, targetZones, anchorPointTargetZoneDict, addressAnchorTimeDict 
    variables. also initializes the songIdDeltaDict to be an empty dictionary with lists as values for future use.
    """

    def initializeAll(self):

        # self.timeFrequencyPoints = [(1, 10), (1, 20), (1, 30), (2, 10), (3, 10), (3, 20), (3, 30), (4, 20), (4, 30),
        #                             (5, 20), (6, 10)]

        self.createConstellationMap()
        self.targetZones = createTargetZones(self.timeFrequencyPoints)
        self.anchorPointTargetZoneDict = createAnchorPoints(self.timeFrequencyPoints, self.targetZones)
        self.createAddresses()
        self.songIdDeltaDict = {address: [] for address in self.addressAnchorTimeDict.keys()}

    """
    function name: createConstellationMap.
    input: N/A
    output: N/A
    operation: initializes the timeFrequencyPoints variable.
    """

    def createConstellationMap(self):
        # sampleRate, data = scipy.io.wavfile.read('C:\PythonProject\Songs\LoseYourself045100R3.wav')
        sampleRate, data = scipy.io.wavfile.read('C:\PythonProject\Songs\AdventureOfALifetime100115R.wav')

        # f, t, Sxx = createSpectrogram(sampleRate, data)
        # self.timeFrequencyPoints, r = filterSpectrogramByRegions(Sxx, f, t, GlobalValues.regionCoefficientR)
        self.timeFrequencyPoints = createFilteredSpectrogramPoints(sampleRate, list(data))

    """
    function name: createAddresses 
    input: N/A 
    output: N/A 
    operation: initializes the addressAnchorTimeDict, 
    for every point in a target zone, calculates the address according to the anchor point. rounds the number to 3 
    decimal points and saves the result as string for the search in the database.    
    """

    def createAddresses(self):
        for anchorPoint, targetZone in self.anchorPointTargetZoneDict.items():
            timeOfAnchor = round(anchorPoint[0], decimalPoints)
            for p in targetZone:
                # tempAddress = (round(anchorPoint[1], decimalPoints) * 1000, round(p[1], decimalPoints) * 1000,
                #                round(p[0] - anchorPoint[0], decimalPoints) * 1000)

                tempAddress = str(int(round(anchorPoint[1], decimalPoints) * 1000)) + ',' + str(
                    int(round(p[1], decimalPoints) * 1000)) + ',' + str(
                    int(round(p[0] - anchorPoint[0], decimalPoints) * 1000))

            if tempAddress in self.addressAnchorTimeDict:
                self.addressAnchorTimeDict[tempAddress].append(timeOfAnchor)
            else:
                self.addressAnchorTimeDict[tempAddress] = [timeOfAnchor]

    '''
    function name: songIdTableUpdate
    input: the value of the database - a list of couples
    output: N/A
    operation: goes through the list, counting the number of couples the song have in common with the address value.
    '''

    def songIdTableUpdate(self, List):
        for couple in List:
            if couple in self.songIdTable:
                self.songIdTable[couple] += 1
            else:
                self.songIdTable[couple] = 1

    '''
    function name: songIdTableFilter 
    input: N/A 
    output: N/A 
    operation: we go through the songIdTable, removing 
    all the couples who's value is less than 4 (i.e couldn't form a target zone), than we goes through the 
    songIdTable again, counting the number of time each songId appeared in a key (a couple) of the hash table (
    putting it in a new hash table). we remove the song whose number is below 300*coefficient, because 300 is the 
    number of target zones in the recording. 
    '''

    def songIdTableFilter(self):
        print(self.songIdTable)
        # self.songIdTable = dict(filter(lambda element: element[1] > 4, self.songIdTable.items()))
        for couple in self.songIdTable.keys():
            if couple[1] in self.songIdNumOfKeysTable.keys():
                self.songIdNumOfKeysTable[couple[1]] += 1
            else:
                self.songIdNumOfKeysTable[couple[1]] = 1

        # self.songIdNumOfKeysTable = dict(
        #     filter(lambda element: element[1] >= 300 * coefficient, self.songIdNumOfKeysTable.items()))


if __name__ == '__main__':
    r = Recording()
    r.initializeAll()

    s = Song('C:\PythonProject\Songs\LoseYourself045100.wav', 'test')
    s.initializeAll()
    print(len(r.timeFrequencyPoints))
    print(r.timeFrequencyPoints)
    # print(len(r.addressAnchorTimeDict))
    # print(len(s.addressCoupleDict))

    #
    #
    # def addressesCreate(self):
    #     for i in range(0, len(self.targetZones)):
    #         if i > 2:
    #             self.anchorPointTargetZoneDict[self.timeFrequencyPoints[i - 3]] = self.targetZones[i]
    #
    #     for anchorPoint in self.anchorPointTargetZoneDict:
    #         for p in self.anchorPointTargetZoneDict[anchorPoint]:
    #             self.addressCouplesList.append(
    #                 (anchorPoint[0], (anchorPoint[1], p[1], p[0] - anchorPoint[0])))
    #
    #     return self.addressCouplesList
