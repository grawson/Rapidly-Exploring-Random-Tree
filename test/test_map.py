from src.Map import Map
import cv2

m = Map("../data/map/obstacles-5.txt", "../data/goal/goal-2.txt")
m.fill()
cv2.imshow("map", m.map)
cv2.waitKey(0)
