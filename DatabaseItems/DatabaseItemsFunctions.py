import GlobalValues

"""
function name: targetZonesCreate.
input: a list of time-frequency points.
output: a list of lists.
operation: creates a list of 5 consecutive points, until it runs out of points. adds that list to the "targetZone" list.
"""


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
    targetSize = GlobalValues.targetSize
    targetZones = []
    for i in range(len(timeFrequencyPoints) - targetSize + 1):
        targetZones.append([timeFrequencyPoints[i + j] for j in range(targetSize)])

    return targetZones


"""
    function name: createAnchorPoints
    input: timeFrequencyPoints - as the name suggest, a list of tuples. targetZones - a list of point lists. 
    output: a dictionary. where the key is an anchor point and the value is a list of points - the target Zone. 
    (5 following points, 3 points to the right [where the positive time axis is to the right] of the anchor point).
    operation: initializes the 'anchorPointTargetZoneDict' variable for the Song and Recording objects.
    """


def createAnchorPoints(timeFrequencyPoints, targetZones):
    return {timeFrequencyPoints[i - 3]: targetZones[i] for i in range(3, len(targetZones))}
