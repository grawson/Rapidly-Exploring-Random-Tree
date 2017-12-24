import numpy as np
import src.const as const

DIM = const.DIM


class TreeNode(object):
    def __init__(self, data, parent=None):
        self.data = data    # tuple (x, y) coordinate
        self.parent = parent
        self.children = list()
        if parent is not None:
            parent.children.append(self)


class TreeMap(object):

    def __init__(self):
        self.map = np.full(DIM, None)
        self.data_list = list()
        self.last_data = None   # the last data added to the tree


    # create a new node and add it to the map
    def add_node(self, data, parent=None):
        if data[0] >= DIM[1] or data[1] >= DIM[0] or data[0] < 0 or data[1] < 0:   # assert bounds
            return False
        if self.find(data) is not None:    # assert not already present
            return False

        self.map[data[1]][data[0]] = TreeNode(data, parent)
        self.data_list.append(data)
        self.last_data = data
        return True


    # return a reference to the node if it's present
    def find(self, data):
        return self.map[data[1]][data[0]]


    # clamp an x, y coordinate to a range
    def clamp(self, point, rnge=DIM):
        clamped_point = [point[0], point[1]]
        for i in range(len(point)):
            clamped_point[i] = max(point[i], 0)
            clamped_point[i] = min(rnge[i]-1, clamped_point[i])
        return clamped_point


    # check if a point is within step_dist of any point in the tree
    def point_in_range(self, point, step_dist):
        start = self.clamp((point[0] - step_dist, point[1] - step_dist))
        end = self.clamp((point[0] + step_dist, point[1] + step_dist))

        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                if self.map[y][x] is not None:
                    return x, y
        return None


    # Return the path from a given up it's parent nodes
    def path(self, node):
        curr_node = node
        path = [curr_node.data]
        while curr_node.parent is not None:
            curr_node = curr_node.parent
            path.insert(0, curr_node.data)
        return path

