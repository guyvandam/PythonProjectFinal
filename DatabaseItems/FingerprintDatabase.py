from ImportsFile import *
from DatabaseItems.Recording import Recording
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

        self.songIdSongInfoDict = {'1': 'Treasure by Bruno Mars',
                                   '2': 'Adventure of a lifetime by Coldplay',
                                   '3': 'Hymn for the weekend by Coldplay',
                                   '4': "darlin' by the Beach boys",
                                   '5': 'Animals by Maroon 5',
                                   '6': 'see you again by Wiz Khalifa'}

        # self.songIdSongInfoDict = songIdSongInfoDict

        # key - songId, value - the song object.
        self.songIdSongObjectDict = {}

        self.songIdAddressCoupleDict = {}

    '''
    function name: loadMany.
    input: a dictionary of paths and songId to be loaded to the fingerprint database.
    output: N/A
    operation: self explanatory. calls the load function for every item in the database.
    '''

    def loadMany(self, pathIdDict):
        self.pullFingerprintDatabase()
        self.pullSongIdAddressCoupleDict()

        for path, songId in pathIdDict.items():
            print("loading songId: ", songId)
            temp = Song(path, songId)
            temp.initializeAll()
            self.databaseUpdateDECIMAL(temp)
            self.songIdAddressCoupleDict[songId] = temp.addressCoupleDict

        self.saveFingerprintDatabase()
        self.saveSongIdAddressCoupleDict()

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

        print("loading songId: ", songId)
        temp = Song(path, songId)
        temp.initializeAll()

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
            # self.database["_id"] = 1
            self.StorageDatabase["_id"] = 1
            # self.collection.insert_one(self.database)
            self.collection.insert_one(self.StorageDatabase)
        except pymongo.errors.DuplicateKeyError:
            print('===== ERROR === KEY EXISTS === ERROR =====')
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
        # self.database = self.collection.find_one({'_id': 1})
        # if self.database is None:
        #     print('===== ERROR === error at find | pullFingerprintDatabase === ERROR =====')
        #     exit(1)
        # # for key,value in self.database.items():
        # # self.database = dict(map(lambda x: tuple(x[0]), self.database.items()))
        # # self.database = {stringToTuple(key): value for key, value in self.database.items()}
        #
        # self.database = {stringToTuple(key): [tuple(v) for v in value] for key, value in self.database.items() if
        #                  not key == '_id'}
        self.StorageDatabase = self.collection.find_one({'_id': 1})
        assert self.StorageDatabase is not None, "===== ERROR === error at find | pullFingerprintDatabase === ERROR " \
                                                 "===== "
        # for key,value in self.database.items():
        # self.database = dict(map(lambda x: tuple(x[0]), self.database.items()))
        # self.database = {stringToTuple(key): value for key, value in self.database.items()}

        self.database = {stringToTuple(key): [tuple(v) for v in value] for key, value in self.StorageDatabase.items() if
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
            # if key in self.database:
            #     self.database[key] += value
            # else:
            #     self.database[key] = value
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
        self.pullFingerprintDatabase()
        self.pullSongIdAddressCoupleDict()
        for address in recording.addressAnchorTimeDict.keys():
            if address in self.database.keys():
                recording.songIdTableUpdate(self.database[address])

        recording.songIdTableFilter()
        return self.filterResults(list(recording.songIdNumOfKeysTable.keys()), recording)

    # time coherency step.
    def filterResults(self, songIdList, recording):
        if len(songIdList) == 0:
            return "didn't find anything :("
        elif len(songIdList) == 1:
            return self.songIdSongInfoDict[songIdList[0]]
        # return self.songIdSongInfoDict[max(recording.songIdNumOfKeysTable.items(), key=lambda tup: tup[1])[0]]

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

                        # if songId in recording.songIdDeltaDict.keys():
                        #     recording.songIdDeltaDict[songId] += deltaList
                        # else:
                        #     recording.songIdDeltaDict[songId] = deltaList

        # finds the delta that appear the most in the list, set the number of appearance to be the new value of the dict
        temp = {key: max(listOfDeltas, key=listOfDeltas.count) for key, listOfDeltas in
                recording.songIdDeltaDict.items()}

        recording.songIdDeltaDict = {key: listOfDeltas.count(temp[key]) for key, listOfDeltas in
                                     recording.songIdDeltaDict.items()}
        print("songIdDeltaDict: ", recording.songIdDeltaDict)
        # prints the songId of the delta the have the max appearances in the delta list.
        return self.songIdSongInfoDict[max(recording.songIdDeltaDict.items(), key=lambda x: x[1])[0]]

    """
    function name: show
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

# if __name__ == '__main__':
#     # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#
#     # database = myclient["mydatabase"]
#     # collection = database["Database collection"]
#
#     pathSongIdDict = {r'C:\PythonProject2\DatabaseSongs\BrunoMarsTreasure.wav': "1",
#                       r'C:\PythonProject2\DatabaseSongs\ColdplayAdventureOfALifetime.wav': "2",
#                       r'C:\PythonProject2\DatabaseSongs\ColdplayHymnForTheWeekend.wav': "3",
#                       r'C:\PythonProject2\DatabaseSongs\Darlin.wav': "4",
#                       r'C:\PythonProject2\DatabaseSongs\Maroon5Animals.wav': "5",
#                       r'C:\PythonProject2\DatabaseSongs\WizKhalifaSeeYouAgain.wav': "6"}
#     fingerprintDatabase = FingerprintDatabase()
#     # fingerprintDatabase.createNewDatabase()
#     fingerprintDatabase.showCollection()
#     # fingerprintDatabase.loadMany(pathSongIdDict)
#
# # songIdSongInfoDict = {'1': 'Treasure by Bruno Mars',
# #                       '2': 'Adventure of a lifetime by Coldplay',
# #                       '3': 'Hymn for the weekend by Coldplay',
# #                       '4': "darlin' by the Beach boys",
# #                       '5': 'Animals by Maroon 5',
# #                       '6': 'see you again by Wiz Khalifa'}
#
# # fingerprintDB = FingerprintDatabase()
# # fingerprintDatabase.load(r'C:\PythonProject2\DatabaseSongs\BrunoMarsTreasure.wav', '1')
# # fingerprintDatabase.load(r'C:\PythonProject2\DatabaseSongs\ColdplayAdventureOfALifetime.wav', '2')
# # fingerprintDB.load(r'C:\PythonProject2\DatabaseSongs\ColdplayHymnForTheWeekend.wav','3')
# # fingerprintDB.showCollection()
#
#     r = Recording("blah")
#     r.initializeAll()
#     fingerprintDatabase.searchInDatabase(r)
