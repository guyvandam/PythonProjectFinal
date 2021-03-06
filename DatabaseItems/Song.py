from ImportsFile import *

decimalPoints = GlobalValues.decimalPoints


class Song:

    def __init__(self, path, songID):
        self.path = path
        self.songID = songID
        # a list of 2-item-tuples
        self.timeFrequencyPoints = []
        # list of lists of points.
        self.targetZones = []
        # key - anchor point, value - target zone
        self.anchorPointTargetZoneDict = {}
        # key - address, value - a list of couple associated with this address.
        self.addressCoupleDict = {}

    """
       function name: initializeAll.
       input: N/A
       output: N/A
       operation: initializes the timeFrequencyPoints, targetZones, anchorPointTargetZoneDict, addressCoupleDict 
       variables. 
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
        operation: initializes the timeFrequencyPoints variable. it reads the wave file associated with the song 
        instance and prepares the data for the fft. 
    """

    def createConstellationMap(self):

        try:
            sampleRate, data = wavefile.read(self.path)
            sampleRate, data = prepareForSpectrogram(sampleRate, data)
            self.timeFrequencyPoints = createFilteredSpectrogramPoints(data)
        except Exception as wavFileException:
            print("error in reading the wav file for path:", self.path)
            raise wavFileException
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
                delta = p[0] - anchorPoint[0]
                tempAddress = str(int(anchorPoint[1])) + ',' + str(int(p[1])) + ',' + str(
                    int(round(delta, decimalPoints) * 10))

                if tempAddress in self.addressCoupleDict:
                    self.addressCoupleDict[tempAddress].append(couple)
                else:
                    self.addressCoupleDict[tempAddress] = [couple]
