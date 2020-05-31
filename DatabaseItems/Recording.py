from ImportsFile import *

decimalPoints = GlobalValues.decimalPoints
coefficient = GlobalValues.songIdFilterCoefficient


class Recording:
    def __init__(self, path):
        self.timeFrequencyPoints = []

        # a list of lists of points.
        self.targetZones = []

        # key - anchor point, value - target zone
        self.anchorPointTargetZoneDict = {}

        # self.addressCouplesList = []

        self.addressAnchorTimeDict = {}

        # key - couple, value - the number of time it appears in the recording address.
        self.songIdTable = {}

        # key - songId, value - the number of time is part of a key in the songIdTable
        self.songIdNumOfKeysTable = {}

        # key - songId, value - a list of deltas of the anchor time for each songId.
        self.songIdDeltaDict = {}

        # the path to the wav file of that recording.
        self.dataPath = path

    """
    function name: initializeAll.
    input: N/A
    output: N/A
    operation: initializes the timeFrequencyPoints, targetZones, anchorPointTargetZoneDict, addressAnchorTimeDict 
    variables. also initializes the songIdDeltaDict to be an empty dictionary with lists as values for future use.
    """

    def initializeAll(self):
        self.createConstellationMap()
        self.targetZones = createTargetZones(self.timeFrequencyPoints)
        self.anchorPointTargetZoneDict = createAnchorPoints(self.timeFrequencyPoints, self.targetZones)
        self.createAddresses()

    """
    function name: createConstellationMap.
    input: N/A
    output: N/A
    operation: initializes the timeFrequencyPoints variable.
    """

    def createConstellationMap(self):
        try:
            sampleRate, data = scipy.io.wavfile.read(self.dataPath)
            self.timeFrequencyPoints = createFilteredSpectrogramPoints(list(data))
        except:
            print("error in reading the wav file...")

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
                delta = p[0] - anchorPoint[0]
                tempAddress = (anchorPoint[1], p[1], int(round(delta, decimalPoints) * 10))

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
    all the couples who's value is less than 2, than we go through the 
    songIdTable again, counting the number of time each songId appeared in a key (a couple) of the hash table (
    putting it in a new hash table). we remove the song whose number is below 20*coefficient.
    '''

    def songIdTableFilter(self):

        if self.songIdTable:
            self.songIdTable = dict(filter(lambda element: element[1] > 1, self.songIdTable.items()))

        if not self.songIdTable:
            return

        for couple in self.songIdTable.keys():
            if couple[1] in self.songIdNumOfKeysTable.keys():
                self.songIdNumOfKeysTable[couple[1]] += 1
            else:
                self.songIdNumOfKeysTable[couple[1]] = 1

        self.songIdNumOfKeysTable = dict(
            filter(lambda element: element[1] >= 20 * coefficient, self.songIdNumOfKeysTable.items()))
