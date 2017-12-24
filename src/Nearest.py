from scipy.spatial import distance
import sys


# Return the nearest neighbor to z.
def nearest_neighbors(points, z_point):
    min_dist, min_point = sys.maxint, None
    for point in points:
        dist = distance.euclidean(point, z_point)
        if dist < min_dist:
            min_dist = dist
            min_point = point
    return min_point
