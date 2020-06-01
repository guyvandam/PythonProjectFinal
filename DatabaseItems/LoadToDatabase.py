"""
program for loading songs into the database.
"""
from DatabaseItems.FingerprintDatabase import FingerprintDatabase

Database = FingerprintDatabase()

songIdSongInfoDict = {}
songIdPathDict = {}

print("to stop the loop enter 0 for any of the input boxes\n")
loopCondition = 1
while loopCondition:
    path = input("enter the path to the wav file\n")
    if path == '0':
        break

    songId = input("enter the song Id\n")
    if songId == '0':
        break

    songInfo = input("enter the song Information, this will be shown to the user as the song metadata\n")
    if songInfo == '0':
        break

    songIdPathDict[songId] = path
    songIdSongInfoDict[songId] = songInfo

Database.loadMany(songIdPathDict, songIdSongInfoDict)
