def createPoints(x, y):
    return [(x[i], y[i]) for i in range(0, len(x))]


def createLists(points):
    return [p[0] for p in points], [p[1] for p in points]
