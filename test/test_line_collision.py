import numpy as np
import cv2
from scipy.spatial import distance

img = np.zeros((600, 600, 3), dtype=np.uint8)


# Get the point on a line between two points at a certain step
# when t=0, point=p1. when t=1, point=p2
def parametric_point(p1, p2, t):
    x = p1[0] + (p2[0] - p1[0]) * t
    y = p1[1] + (p2[1] - p1[1]) * t
    return int(round(x)), int(round(y))


def is_line_collision(p1, p2):
    is_line_collision_recur(p1, p2, 0)


def is_line_collision_recur(p1, p2, depth, factor=0.5, max_depth=8):
    global img

    if depth == max_depth: return False

    curr_t = 0
    while curr_t <= 1:
        point = parametric_point(p1, p2, curr_t)
        curr_t += factor
        cv2.circle(img, point, 1, (100, 100, 100), -1)
        cv2.imshow("line", img)
        cv2.waitKey(2)

    return is_line_collision_recur(p1, p2, depth+1, factor/2.0, max_depth)


point1, point2 = (20, 20), (500, 20)
cv2.circle(img, point1, 1, (0, 255, 0), -1)
cv2.circle(img, point2, 1, (0, 255, 0), -1)
is_line_collision(point1, point2)
cv2.waitKey(0)
