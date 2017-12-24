
import cv2
import numpy as np
import src.const as const

CHECK_SPECIAL_CASES = False
# BOUNDARY_COLOR = (0, 0, 255)
BOUNDARY_COLOR = (0, 0, 0)


class Obstacle:

    def __init__(self, vertices):
        self.max_x, self.min_x, self.max_y, self.min_y = None, None, None, None
        self.vertices = np.array(vertices)    # note that vertices are in x,y (c,r) order
        self.find_bounding_box()

    # PUBLIC #######################################################################################################

    # check if an obstacle contains a point
    def contains_point(self, point):

        # Optimize by first checking bounding box
        if not self.in_bounding_box(point):
            return False

        j = -1
        inside = False
        for i in range(len(self.vertices)):
            x_i, y_i = self.vertices[i][0], self.vertices[i][1]
            x_j, y_j = self.vertices[j][0], self.vertices[j][1]
            x, y = point[0], point[1]

            # check for intersection
            intrsect = ((y_i > y) != (y_j > y)) and (x < (x_j - x_i) * (y - y_i) / (y_j - y_i) + x_i)

            if intrsect:
                inside = not inside
            j += 1
        return inside


    # Draw the obstacle on the map
    def draw_obstacle(self, img):
        for i in range(len(self.vertices)-1):
            cv2.line(img, tuple(self.vertices[i]), tuple(self.vertices[i+1]), BOUNDARY_COLOR, thickness=1)
        cv2.line(img, tuple(self.vertices[0]), tuple(self.vertices[-1]), BOUNDARY_COLOR, thickness=1)


    # PRIVATE ######################################################################################################

    # Calculate vertices of the obstacle's bounding box
    def find_bounding_box(self):
        maxima = np.amax(self.vertices, axis=0)
        self.max_x = maxima[0]
        self.max_y = maxima[1]

        minima = np.amin(self.vertices, axis=0)
        self.min_x = minima[0]
        self.min_y = minima[1]


    # Check if a point is within the obstacle's bounding box
    def in_bounding_box(self, point):
        return not (point[0] < self.min_x or point[0] > self.max_x or point[1] < self.min_y or point[1] > self.max_y)


    def draw_bounding_box(self, img):
        cv2.circle(img, (self.max_x, self.max_y), 2, (0, 255, 0))
        cv2.circle(img, (self.max_x, self.min_y), 2, (0, 255, 0))
        cv2.circle(img, (self.min_x, self.max_y), 2, (0, 255, 0))
        cv2.circle(img, (self.min_x, self.min_y), 2, (0, 255, 0))
