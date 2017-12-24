from Obstacle import Obstacle
import numpy as np
import time
import cv2
import src.const as const

DIM = (const.DIM[0], const.DIM[1], 3)
BLANK_PX = (53, 42, 40)
FILLED_PX = (200, 200, 200)


class Map:

    # INIT #########################################################################################################

    def __init__(self, obstacles_file, endpoints_file):
        self.obstacles = list()
        self.map = np.full(DIM, BLANK_PX, dtype=np.uint8)
        self.start, self.goal = None, None
        self.init_endpoints(endpoints_file)
        self.init_obstacles(obstacles_file)
        self.draw_obstacles()
        self.draw_endpoints()


    # PUBLIC #######################################################################################################

    # Fill map ensuring no collisions with obstacles.
    def fill(self):
        print "Checking for obstacles and filling map..."
        start = time.time()
        points = [[int(val / DIM[0]), int(val % DIM[1])] for val in range(DIM[0] * DIM[1])]
        for point in points:
            if point[0] % 50 == 0 and point[1] == 0: print "Filling point: " + str(point)
            if all([not obstacle.contains_point(point) for obstacle in self.obstacles]):
                self.map[point[1]][point[0]] = FILLED_PX
        print "Filled map in: " + str(time.time() - start) + "s"
        self.draw_endpoints()


    # FUNC #########################################################################################################

    # Init start and goal points from file.
    def init_endpoints(self, endpoints_file):
        endpoints = list()
        for line in open(endpoints_file, "r"):
            line = line.strip().split(" ")
            line = [int(i) for i in line]   # Convert values to ints
            endpoints.append(line)
        self.start = tuple(endpoints[0])
        self.goal = tuple(endpoints[1])


    # Initialize the obstacles in the map based on an obstacles text file
    def init_obstacles(self, obstacles_file):
        vertices = list()
        for line in open(obstacles_file, "r"):
            line = line.strip().split(" ")
            line = [int(i) for i in line]   # Convert values to ints

            # new obstacle encountered. Save current vertices as an obstacle and reset vertices
            if len(line) == 1:
                if len(vertices) > 0:
                    self.obstacles.append(Obstacle(vertices))
                vertices = list()

            # New vertex encountered
            else:
                vertices.append(line)
        self.obstacles.append(Obstacle(vertices))  # add the last object in the file

    # Draw all the obstacles onto the map
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw_obstacle(self.map)


    # draw start and end points
    def draw_endpoints(self):
        cv2.circle(self.map, self.start, 4, (70, 187, 95), thickness=-1)
        cv2.circle(self.map, self.goal, 4, (46, 72, 239), thickness=-1)


    # Chekc if a point collides with any objects
    def is_point_collision(self, (x, y)):
        for obstacle in self.obstacles:
            if obstacle.contains_point((x, y)):
                return True
        return False


    # Get the point on a line between two points at a certain step
    # when t=0, point=p1. when t=1, point=p2
    def parametric_point(self, p1, p2, t):
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        return int(round(x)), int(round(y))


    # sample points on the line at t_steps of <factor>
    def is_line_collision(self, p1, p2, depth=0, factor=0.5, max_depth=8):
        if depth == max_depth: return False

        curr_t = 0
        while curr_t <= 1:
            point = self.parametric_point(p1, p2, curr_t)
            if self.is_point_collision(point):  # check sampled point for collision
                return True
            curr_t += factor
        return self.is_line_collision(p1, p2, depth + 1, factor / 2.0, max_depth)  # halve the factor

