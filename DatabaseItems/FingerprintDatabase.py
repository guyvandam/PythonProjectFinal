from ImportsFile import *


def stringToTuple(s):
    try:
        return tuple(map(float, s.split(',')))
    except Exception:
        return s


class FingerprintDatabase:
    def __init__(self, Collection):
        # key - an address, value - a list of couples matching the key.
        self.database = {}

        # key - songId, value - the song object.
        self.songIdSongObjectDict = {}

        self.songIdAddressCoupleDict = {}

        self.collection = Collection

    # '''
    # function name: loadMany.
    # input: a dictionary of paths and songId to be loaded to the fingerprint database.
    # output: N/A
    # operation: self explanatory. calls the load function for every item in the database.
    # '''
    #
    # def loadMany(self, pathIdDict):
    #     self.pullFingerprintDatabase()
    #     for path, songId in pathIdDict.items():
    #         temp = Song(path, songId)
    #         temp.initializeAll()
    #
    #         self.databaseUpdateDECIMAL(temp)
    #         self.songIdAddressCoupleDict[songId] = temp.addressCoupleDict
    #
    #     self.saveFingerprintDatabase()

    ''' 
    function name: load.
    input: path, the song id.
    output: N/A
    operation: creates the address for the point in the address object, load them in the "database" dictionary,
    if a key already exist, adds the match couple to the value (a list) of the key, if not, creates a new key and a list
    of one object, so it can be expanded in the future.
    '''

    def load(self, path, songId):

        self.pullFingerprintDatabase()
        self.pullSongIdAddressCoupleDict()
        temp = Song(path, songId) # ==========================================================================================
        temp.initializeAll()
        print(temp.songID)

        self.databaseUpdateDECIMAL(temp)

        self.songIdAddressCoupleDict[songId] = temp.addressCoupleDict

        self.saveFingerprintDatabase()
        self.saveSongIdAddressCoupleDict()

    '''
    function name: saveDatabase.
    input: N/A
    output: N/A
    operation: saves the database changes to memory.
    '''

    def saveFingerprintDatabase(self):
        self.collection.delete_one({"_id": 1})
        try:
            self.collection.insert_one(self.database)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === KEY EXISTS === ERROR =====')
        else:
            print('===== SAVED SUCCESSFULLY =====')

    '''
    function name: pullDatabase
    input: N/A
    output: N/A
    operation: pulls the database from memory so we can alter it.
    '''

    def pullFingerprintDatabase(self):
        self.database = self.collection.find_one({'_id': 1})
        if self.database is None:
            print('===== ERROR === error at find | pullFingerprintDatabase === ERROR =====')
            exit(1)
        # for key,value in self.database.items():
        # self.database = dict(map(lambda x: tuple(x[0]), self.database.items()))
        # self.database = {stringToTuple(key): value for key, value in self.database.items()}
        self.database = {stringToTuple(key): [tuple(v) for v in value] for key, value in self.database.items() if
                         not key == '_id'}
        '''
        function name: saveSongIdAddressCoupleDict
        input: N/A
        output: N/A
        operation: saves the songIdDict to changes to memory.
        '''

    def saveSongIdAddressCoupleDict(self):
        self.collection.delete_one({"_id": 2})
        try:
            self.collection.insert_one(self.songIdAddressCoupleDict)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === KEY EXISTS === ERROR =====')
        else:
            print('===== SAVED SUCCESSFULLY =====')

    '''
    function name: pullSongIdAddressCoupleDict
    input: N/A
    output: N/A
    operation: pulls the songIdAddressCoupleDict from memory
    '''

    def pullSongIdAddressCoupleDict(self):
        self.songIdAddressCoupleDict = self.collection.find_one({"_id": 2})
        if self.database is None:
            print('===== ERROR === error at find_one === ERROR =====')
            exit(1)

    '''
    function name: databaseUpdateDECIMAL
    input: a song object
    output: N/A
    operation:  ==========a regular "decimal" method for checking and demonstration==========
    creates the address for the point in the address object, load them in the "database" dictionary,
    if a key already exist, adds the match couple to the value (a list) of the key, if not, creates a new key and a list
    of one object, so it can be expanded in the future.
    '''

    def databaseUpdateDECIMAL(self, song):
        addressCoupleDict = song.addressCoupleDict
        for key, value in addressCoupleDict.items():  # the key is an address
            if key in self.database:
                self.database[key] += value
            else:
                self.database[key] = value

    '''
    function name: searchInDatabase
    input: the recoding list of addresses and couples
    output: N/A
    operation: if an address is in the database, the function updates the songIdTable.
    '''

    def searchInDatabase(self, recording):
        # breakpoint()
        for address in recording.addressAnchorTimeDict.keys():
            if address in self.database.keys():
                recording.songIdTableUpdate(self.database[address])

        recording.songIdTableFilter()
        self.filterResults(list(recording.songIdNumOfKeysTable.keys()), recording)

    # time coherency step.
    def filterResults(self, songIdList, recording):
        if len(songIdList) == 0:
            print("didn't find anything :(")
            exit(1)
        if len(songIdList) == 1:
            print(songIdList[0])
            exit(0)

        for songId in songIdList:
            for address, anchorTimeList in recording.addressAnchorTimeDict.items():
                for anchorTime in anchorTimeList:
                    recording.songIdDeltaDict[songId] += [abs(anchorTime - couple[0]) for couple in
                                                          self.songIdAddressCoupleDict[songId][address]]

        # finds the delta that appear the most in the list, set the number of appearance to be the new value of the dict
        recording.songIdDeltaDict = {key: max(listOfDeltas, key=listOfDeltas.count) for key, listOfDeltas in
                                     recording.songIdDeltaDict.items()}
        # prints the songId of the delta the have the max appearances in the delta list.
        print(max(recording.songIdDeltaDict, key=lambda x: x[1]))

    def showCollection(self):
        for x in self.collection.find():
            print(x)
            print(len(x))


if __name__ == '__main__':
    import pymongo

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    database = myclient["mydatabase"]
    collection = database["Database collection"]

    # collection.drop()
    # collection.insert_one({"_id": 1})
    # collection.insert_one({"_id": 2})

    fingerprintDB = FingerprintDatabase(collection)

    # fingerprintDB.load('C:\PythonProject\Songs\LoseYourself030200S.wav','1')
    # fingerprintDB.showCollection()
    fingerprintDB.pullFingerprintDatabase()
    fingerprintDB.showCollection()
    r = Recording()
    r.initializeAll()
    # r.plotConstellationMap()

    fingerprintDB.searchInDatabase(r)
