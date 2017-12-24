from src.Map import Map
from src.TreeMap import TreeMap
from src.Nearest import nearest_neighbors
from src.Line import line_function
import cv2
import numpy as np
import sys
import random
import time
from scipy.spatial import distance
import src.const as const
import argparse



# VAR ########################################

DIM = const.DIM
TREE_COLORS = [(141, 208, 178), (141, 154, 246)]

STEP = False     # True if user must click a key to go to next step
SAVE_MODE = False

# FUNC #######################################


# create a random point
def get_random_point():
    return random.randint(0, DIM[0]), random.randint(0, DIM[1])


# grow the rrt by one node as long as there is no collision. return data of node created
# bias = the coordinate to set as q_rand. if null, q_rand will be set randomly
def grow_tree(iteration, mapp, tree_map, step_dist, color, bias_pos=None):

    # init random point, find the nearest neighbor in the tree, and step <DIST> from the nearest neighbor to rand point
    q_rand = get_random_point() if bias_pos is None else bias_pos
    nearest_data = nearest_neighbors(tree_map.data_list, q_rand)
    q_step = line_function(step_dist, nearest_data, q_rand)

    # Ensure we found a q_step
    if q_step is None: return False

    # check bounds for q_step
    if any([i < 0 for i in q_step]) or any([q_step[i] >= const.DIM[i] for i in range(len(q_step))]):
        return False

    # check for existance
    if tree_map.find(q_step) is not None: return False

    # Ensure there is no collision between the start point and q_step
    if mapp.is_line_collision(nearest_data, q_step):
        return False

    # add the step point to the tree
    nearest_node = tree_map.find(nearest_data)
    tree_map.add_node(q_step, nearest_node)

    # update image
    cv2.circle(mapp.map, q_step, 2, color, -1)
    cv2.line(mapp.map, q_step, nearest_data, color)

    # For debugging line function
    if STEP:
        test_img = np.zeros((DIM[0], DIM[1], 3), dtype=np.uint8)
        cv2.circle(test_img, nearest_data, 3, (0, 0, 255), -1)
        cv2.circle(test_img, q_rand, 3, (0, 0, 255), -1)
        cv2.line(test_img, nearest_data, q_rand, (30, 30, 30))
        cv2.circle(test_img, q_step, 3, (0, 255, 0), -1)
        cv2.imshow("Line", test_img)
    return True


# check if two points are within range of eachother
def points_in_range(p1, p2, step_dist):
    return distance.euclidean(p1, p2) <= step_dist


# Draw the path to the goal
def display_path(path, mapp):
    for i in range(len(path)):
        cv2.circle(mapp.map, path[i], 3, (255, 255, 0), -1)
        # if i + 1 < len(path):
        #     cv2.line(mapp.map, path[i], path[i + 1], (255, 40, 40))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="The step distance for tree growing", type=int, dest="step_dist", required=True)
    parser.add_argument('--bidirectional', help="Grow two trees and connect when they near each other", action='store_true', dest="bidirectional")
    parser.add_argument('--debug', help="Show growing animation", dest="debug", action='store_true')
    parser.add_argument('--map', help="Map file in the data/goal folder", dest="map", default='obstacles-1.txt')
    parser.add_argument('--goal', help="File in the data/map folder containing start and end coordinates", dest="goal", default='goal-1.txt')
    parser.add_argument('--bias', help="Add bias to the tree growing", dest="bias", action='store_true')

    args = parser.parse_args()
    return args.step_dist, args.bidirectional, args.debug, args.map, args.goal, args.bias


##############################################


def main(program_iter):
    step_dist, bidirectional, debug, map_file, goal_file, bias = parse_args()

    # init vars
    expansions = 0
    m = Map("data/map/" + str(map_file), "data/goal/" + str(goal_file))
    tree_maps = [TreeMap(), TreeMap()] if bidirectional else [TreeMap()]
    start = time.time()

    # add start position as root node
    assert m.start is not None and m.goal is not None
    tree_maps[0].add_node(m.start)
    if bidirectional:
        tree_maps[1].add_node(m.goal)

    # continue until the goal is added to the tree
    iteration = 0
    goal_coords = list()    # coordinates of the goal points of each tree (1 if unidirectional, 2 if bidirectional)
    while len(goal_coords) == 0:

        # grow trees
        for i in range(len(tree_maps)):

            # set bias if necessary
            bias_pos = None
            if bias and iteration % 20 == 0:
                bias_pos = m.goal if i == 0 else m.start

            if grow_tree(iteration, m, tree_maps[i], step_dist, TREE_COLORS[i], bias_pos):
                expansions += 1
        iteration += 1

        # if multiple trees, check if they are in range of connecting to one another without a collision
        if bidirectional:

            # endpoints are equal
            if tree_maps[1].find(tree_maps[0].last_data) or tree_maps[0].find(tree_maps[1].last_data):
                goal_coords = [tree_maps[0].last_data, tree_maps[1].last_data]

            # Endpoints are in range
            for i in range(len(tree_maps)):
                next_i = (i+1) % len(tree_maps)
                last_point_this_tree = tree_maps[i].last_data
                close_point_other_tree = tree_maps[next_i].point_in_range(last_point_this_tree, step_dist)

                # Update the goal coordinates if there is no collision when connetcing the points between the 2 trees
                if close_point_other_tree is not None and not m.is_line_collision(last_point_this_tree, close_point_other_tree):
                    goal_coords = [None, None]
                    goal_coords[i] = last_point_this_tree
                    goal_coords[next_i] = close_point_other_tree
                    cv2.line(m.map, goal_coords[0], goal_coords[1], TREE_COLORS[0])

        # Always check if last point added is close to the goal
        if (len(goal_coords) == 0
                and points_in_range(tree_maps[0].last_data, m.goal, step_dist)
                and not m.is_line_collision(tree_maps[0].last_data, m.goal)):
            goal_coords.append(tree_maps[0].last_data)
            cv2.line(m.map, goal_coords[0], m.goal, TREE_COLORS[0])

        # Show image for debugging
        if debug:
            cv2.imshow("Map", m.map)
            key = cv2.waitKey(0 if STEP else 1)
            if ord("q") == key:
                cv2.destroyAllWindows()
                sys.exit()

    # create final path, for unidirectional or bidirectional trees
    full_path = list()
    for i in range(len(goal_coords)):
        goal_node = tree_maps[i].find(goal_coords[i])
        path = tree_maps[i].path(goal_node)
        full_path.extend(list(reversed(path)) if i == 1 else path)  # reverse the path if its from the seconds tree

    # add goal node if not already there (b/c of in range stopping condition checks)
    if full_path[-1] != m.goal:
        full_path.append(m.goal)
    display_path(full_path, m)

    # Show completed map
    if SAVE_MODE:
        filename = "results/map-2/step" + str(step_dist)
        if bias: filename += "_bias"
        if bidirectional: filename += "_bidirec"
        cv2.imwrite(filename + "_trial" + str(program_iter) + ".png", m.map)
    print "Finished in: " + str(round(time.time() - start)) + "s"
    print "Expansions: " + str(expansions)

    if not SAVE_MODE:
        cv2.imshow("Map", m.map)
        cv2.waitKey(0)


if __name__ == '__main__':
    for i in range(1):
        main(i+1)
