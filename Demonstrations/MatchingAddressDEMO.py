from DatabaseItems import Song, Recording

ss = Song.Song(r'C:\PythonProject\Songs\AdventureOfALifetime045200S.wav', 'test')
ss.initializeAll()

sm = Recording.Recording()
sm.initializeAll()

addressS = ss.addressCoupleDict.keys()
addressR = sm.addressAnchorTimeDict.keys()

print('addresses of the song', addressS)
print('addresses of the recording', addressR)

intersectionAddresses = set(addressR).intersection(set(addressS))
print(len(intersectionAddresses))
