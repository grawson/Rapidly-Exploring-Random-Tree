import cv2
import numpy as np
import sys
import argparse

WINDOW = "map"
OFFSET = 30
AXIS_ALIGNED = False


def clicked_img(event, x, y, flags, param):
    global coords, img
    if event == cv2.EVENT_FLAG_LBUTTON:

        if not AXIS_ALIGNED:
            coords.append((x, y))
            if len(coords) >= 2 and coords[-2] is not None:
                cv2.line(img, coords[-1], coords[-2], (0, 200, 30))

        else:
            if len(coords) == 0 or coords[-1] is None:
                coords.append((x, y))
            else:
                last_coord = coords[-1]
                if abs(last_coord[0] - x) <= OFFSET:
                    coords.append((last_coord[0], y))
                    cv2.line(img, last_coord, coords[-1], (0, 200, 30))
                elif abs(last_coord[1] - y) <= OFFSET:
                    coords.append((x, last_coord[1]))
                    cv2.line(img, last_coord, coords[-1], (0, 200, 30))


def close_objects(coords):
    assert len(coords) >= 4
    curr_i = 0
    next_i = 1

    first_v = coords[0]
    while next_i < len(coords):

        if first_v is None:
            first_v = coords[curr_i]

        if coords[next_i] is None:
            last_v = coords[curr_i]

            if abs(last_v[0] - first_v[0]) <= OFFSET:
                coords[curr_i] = (first_v[0], last_v[1])
            elif abs(last_v[1] - first_v[1]) <= OFFSET:
                coords[curr_i] = (last_v[0], first_v[1])

            first_v = None

        curr_i += 1
        next_i += 1


def vertex_counts(coords):
    curr = 0
    counts = list()
    for coord in coords:
        if coord is None:
            counts.append(curr)
            curr = 0
        else:
            curr += 1
    return counts


parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="File to save to in map folder", type=str, dest="map", required=True)
args = parser.parse_args()

coords = list()
img = np.full((600, 600, 3), (0, 0, 0), dtype=np.uint8)
cv2.namedWindow(WINDOW)
cv2.setMouseCallback(WINDOW, clicked_img)

while True:
    key = cv2.waitKey(20) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("c"):
        coords.append(None)
    elif key == ord("s"):

        if AXIS_ALIGNED: close_objects(coords)
        v_counts = vertex_counts(coords)

        curr_obstacle = 0
        outfile = open("data/map/" + str(args.map), "w")
        outfile.write(str(len(v_counts)) + "\n")
        outfile.write(str(v_counts[curr_obstacle]) + "\n")
        curr_obstacle += 1

        for coord in coords:
            if coord is None:
                if curr_obstacle < len(v_counts):
                    outfile.write(str(v_counts[curr_obstacle]) + "\n")
                    curr_obstacle += 1
            else:
                outfile.write(str(coord[0]) + " " + str(coord[1]) + "\n")
        outfile.close()
        cv2.destroyAllWindows
        sys.exit()

    cv2.imshow(WINDOW, img)
cv2.destroyAllWindows()
