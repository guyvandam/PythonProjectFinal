"""
function name: createPoints.
input: x - a list, y - a list. 2 list of the same object and size.
output: a list of tuples.
operation: N/A
"""


def createPoints(x, y):
    return [(x[i], y[i]) for i in range(0, len(x))]


"""
function name: createLists.
input: points - a list of tuples.
output: 2 lists. a list of the first item in the tuples and a list of the second item in the tuples.
operation: N/A.
"""


def createLists(points):
    return [p[0] for p in points], [p[1] for p in points]
