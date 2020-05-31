from ImportsFile import *
from DatabaseItems.Song import Song
import pymongo


def stringToTuple(s):
    try:
        return tuple(map(float, s.split(',')))
    except Exception:
        return s


def addressToString(tup):
    return str(tup[0]) + ',' + str(tup[1]) + ',' + str(tup[2])


class FingerprintDatabase:
    def __init__(self):
        myClient = pymongo.MongoClient("mongodb://localhost:27017/")

        myDataBase = myClient["mydatabase"]
        self.collection = myDataBase["Database collection"]

        # key - an address, value - a list of couples matching the key.
        self.database = {}

        self.StorageDatabase = {}

        self.songIdSongInfoDict = {}

        self.songIdAddressCoupleDict = {}

    '''
    function name: loadMany.
    input: a dictionary of paths and songId to be loaded to the fingerprint database.
    output: N/A
    operation: self explanatory. calls the load function for every item in the database.
    '''

    def loadMany(self, songIdPathDict, songIdInfoDict):
        self.pullAll()

        for songId, path in songIdPathDict.items():
            print("loading:", songIdInfoDict[songId])
            temp = Song(path, songId)
            temp.initializeAll()
            self.databaseUpdate(temp)
            self.songIdAddressCoupleDict[songId] = temp.addressCoupleDict
            self.songIdSongInfoDict[songId] = songIdInfoDict[songId]

        self.pushAll()

    ''' 
    function name: load.
    input: path, the song id.
    output: N/A
    operation: creates the address for the point in the address object, load them in the "database" dictionary,
    if a key already exist, adds the match couple to the value (a list) of the key, if not, creates a new key and a list
    of one object, so it can be expanded in the future.
    '''

    def load(self, path, songId, songInfo):
        self.pullAll()

        print("loading: ", songInfo)
        temp = Song(path, songId)
        temp.initializeAll()

        self.databaseUpdate(temp)
        self.songIdAddressCoupleDict[songId] = temp.addressCoupleDict
        self.songIdSongInfoDict[songId] = songInfo

        self.pushAll()

    '''
    function name: saveDatabase.
    input: N/A
    output: N/A
    operation: saves the database changes to memory.
    '''

    def pushFingerprintDatabase(self):
        self.collection.delete_one({"_id": 1})
        try:
            self.StorageDatabase["_id"] = 1
            self.collection.insert_one(self.StorageDatabase)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === DuplicateKeyError for dict 1 === ERROR =====')
            exit(1)
        else:
            print('===== FINGERPRINT DATABASE SAVED SUCCESSFULLY =====')

    '''
    function name: pullDatabase
    input: N/A
    output: N/A
    operation: pulls the database from memory so we can alter it.
    '''

    def pullFingerprintDatabase(self):
        self.StorageDatabase = self.collection.find_one({"_id": 1})
        assert self.StorageDatabase, "===== ERROR === error at pullFingerprintDatabase === ERROR ===== "
        self.database = {stringToTuple(key): [tuple(v) for v in value] for key, value in self.StorageDatabase.items() if
                         not key == '_id'}

    '''
    function name: saveSongIdAddressCoupleDict
    input: N/A
    output: N/A
    operation: saves the songIdDict to changes to memory.
    '''

    def pushSongIdAddressCoupleDict(self):
        self.collection.delete_one({"_id": 2})
        try:
            self.collection.insert_one(self.songIdAddressCoupleDict)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === DuplicateKeyError for dict 2 === ERROR =====')
        else:
            print('===== SongIdAddressCoupleDict SAVED SUCCESSFULLY =====')

    '''
    function name: pullSongIdAddressCoupleDict
    input: N/A
    output: N/A
    operation: pulls the songIdAddressCoupleDict from memory
    '''

    def pullSongIdAddressCoupleDict(self):
        self.songIdAddressCoupleDict = self.collection.find_one({"_id": 2})
        assert self.songIdAddressCoupleDict, "===== ERROR === error at pullFingerprintDatabase === ERROR ===== "

    """
    function name: pushSongIdSongInfoDict.
    input: N/A
    output: N/A.
    operation: saves the songIdSongInfoDict to memory.
    """

    def pushSongIdSongInfoDict(self):
        self.collection.delete_one({"_id": 3})
        try:
            self.collection.insert_one(self.songIdSongInfoDict)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === DuplicateKeyError for dict 3 === ERROR =====')
        else:
            print('===== SongIdSongInfoDict SAVED SUCCESSFULLY =====')

    """
    function name: pullSongIdSongInfoDict.
    input: N/A
    output: N/A.
    operation: pulls the songIdSongInfoDict from memory.
    """

    def pullSongIdSongInfoDict(self):
        self.songIdSongInfoDict = self.collection.find_one({"_id": 3})
        assert self.songIdSongInfoDict, "===== ERROR === error at pullSongIdSongInfoDict === ERROR " \
                                        "===== "

    """
   function name: pullAll.
   input: N/A
   output: N/A.
   operation: pulls the fingerprintDatabase, SongIdAddressCoupleDict and songIdSongInfoDict from memory.
   """

    def pullAll(self):
        self.pullFingerprintDatabase()
        self.pullSongIdAddressCoupleDict()
        self.pullSongIdSongInfoDict()

    """
    function name: pushAll.
    input: N/A
    output: N/A.
    operation: saves the fingerprintDatabase, SongIdAddressCoupleDict and songIdSongInfoDict to memory.
    """

    def pushAll(self):
        self.pushFingerprintDatabase()
        self.pushSongIdAddressCoupleDict()
        self.pushSongIdSongInfoDict()

    '''
    function name: databaseUpdateDECIMAL
    input: a song object
    output: N/A
    operation:  ==========a regular "decimal" method for checking and demonstration==========
    creates the address for the point in the address object, load them in the "database" dictionary,
    if a key already exist, adds the match couple to the value (a list) of the key, if not, creates a new key and a list
    of one object, so it can be expanded in the future.
    '''

    def databaseUpdate(self, song):
        addressCoupleDict = song.addressCoupleDict
        for key, value in addressCoupleDict.items():  # the key is an address
            if key in self.StorageDatabase:
                self.StorageDatabase[key] += value
            else:
                self.StorageDatabase[key] = value

    '''
    function name: searchInDatabase
    input: the recoding list of addresses and couples
    output: N/A
    operation: if an address is in the database, the function updates the songIdTable.
    '''

    def searchInDatabase(self, recording):
        self.pullAll()
        for address in recording.addressAnchorTimeDict.keys():
            if address in self.database.keys():
                recording.songIdTableUpdate(self.database[address])

        recording.songIdTableFilter()
        return self.filterResults(list(recording.songIdNumOfKeysTable.keys()), recording)

    """
    function name: filterResults.
    input: songIdList - self explnetory, recording - a Recording object, the recording in the search.
    output: the information for the song we predict the recording matches to. (if we can make such prediction).
    operation: now for each song id (the key) we'll find the delta that appears most in that list. we'll save the time 
    of appearances, and the song with the most appearances we'll be our prediction.  
    """

    def filterResults(self, songIdList, recording):
        if len(songIdList) == 0:
            return "didn't find anything :("
        elif len(songIdList) == 1:
            return self.songIdSongInfoDict[songIdList[0]]

        # initialize the songIdDeltaDict for future use.
        recording.songIdDeltaDict = {songId: [] for songId in songIdList}

        for songId in songIdList:
            for address, anchorTimeList in recording.addressAnchorTimeDict.items():
                for anchorTime in anchorTimeList:

                    tempAddressCoupleDict = self.songIdAddressCoupleDict[songId]
                    stringAddress = addressToString(address)
                    if stringAddress in tempAddressCoupleDict.keys():
                        deltaList = [abs(anchorTime - couple[0]) for couple in tempAddressCoupleDict[stringAddress]]
                        recording.songIdDeltaDict[songId] += deltaList

        # finds the delta that appear the most in the list, set the number of appearance to be the new value of the dict
        temp = {key: max(listOfDeltas, key=listOfDeltas.count) for key, listOfDeltas in
                recording.songIdDeltaDict.items()}

        recording.songIdDeltaDict = {key: listOfDeltas.count(temp[key]) for key, listOfDeltas in
                                     recording.songIdDeltaDict.items()}
        prediction = self.songIdSongInfoDict[max(recording.songIdDeltaDict.items(), key=lambda x: x[1])[0]]
        return prediction

    """
    function name: showCollection.
    input: N/A
    output: N/A
    operation: prints the 2 dictionaries in the collection.
    """

    def showCollection(self):
        for x in self.collection.find():
            print(x)
            print(len(x))

    """
    function name: createNewDatabase.
    input: N/A
    output: N/A
    operation: deletes the old database (the mongoDB collection) and inserts new dictionaries for the future database.
    """

    def createNewDatabase(self):
        self.collection.drop()
        self.collection.insert_one({"_id": 1})
        self.collection.insert_one({"_id": 2})
        self.collection.insert_one({"_id": 3})
