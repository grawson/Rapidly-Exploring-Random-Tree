from scipy.spatial import distance


# Get the point on a line between two points at a certain step
# when t=0, point=p1. when t=1, point=p2
def parametric_point(p1, p2, t):
    x = p1[0] + (p2[0] - p1[0]) * t
    y = p1[1] + (p2[1] - p1[1]) * t
    return int(round(x)), int(round(y))


def line_function(step_size, start_point, end_point):
    line_length = distance.euclidean(start_point, end_point)
    return None if step_size > line_length else parametric_point(start_point, end_point, step_size/float(line_length))

