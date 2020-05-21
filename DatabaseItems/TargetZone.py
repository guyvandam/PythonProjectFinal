'''
function name: targetZonesCreate.
input: a list of time-frequency points.
output: a list of lists.
operation: creates a list of 5 consecutive points, until it runs out of points. adds that list to the "targetZone" list.
'''


def createTargetZones(timeFrequencyPoints):
    # i = 0
    # targetZones = []
    # targetSize = 5
    # while i < len(time_frequencyPoints):
    #     temp = []
    #     j = i
    #
    #     while j < targetSize + i <= len(time_frequencyPoints) and j < len(time_frequencyPoints):
    #         temp.append(time_frequencyPoints[j])
    #         j += 1
    #
    #     if temp:
    #         targetZones.append(temp)
    #
    #     i += 1
    #
    # return targetZones
    targetSize = 5
    targetZones = []
    for i in range(len(timeFrequencyPoints) - targetSize + 1):
        targetZones.append([timeFrequencyPoints[i + j] for j in range(targetSize)])

    return targetZones


def timeFrequencyPointsCreateDEMONSTRATION():
    timeFrequencyPoints = [1, 2, 3, 4, 5]
    targetSize = 3

    targetZones = []
    for i in range(len(timeFrequencyPoints) - targetSize + 1):
        targetZones.append([timeFrequencyPoints[i + j] for j in range(targetSize)])

    print(targetZones)


# def updateDict(tup):
#     songID = '3'
#     addressCouplesDict = {}
#     anchorPoint, targetZone = tup
#     couple = (anchorPoint[0], songID)
#     for p in targetZone:
#         tempAddress = (anchorPoint[1], p[1], p[0] - anchorPoint[0])
#
#     if tempAddress in addressCouplesDict:
#         addressCouplesDict[tempAddress].append(couple)
#     else:
#         addressCouplesDict[tempAddress] = [couple]
#
# def createAddress(self):


