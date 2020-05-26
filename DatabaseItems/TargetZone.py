import GlobalValues

"""
function name: targetZonesCreate.
input: a list of time-frequency points.
output: a list of lists.
operation: creates a list of 5 consecutive points, until it runs out of points. 
adds that list to the "targetZone" list.
"""


def createTargetZones(timeFrequencyPoints):
    targetSize = GlobalValues.targetSize
    targetZones = []
    for i in range(len(timeFrequencyPoints) - targetSize + 1):
        targetZones.append([timeFrequencyPoints[i + j] for j in range(targetSize)])

    return targetZones


