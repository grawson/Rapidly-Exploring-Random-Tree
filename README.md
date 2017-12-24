## To Run

Main driver is `driver.py`. You can customize the following arguments:
```
--step <dist>       The step distance for tree growing
--bidirectional     Grow two trees and connect when they near each other (optional)
--debug             Show growing animation (optional)
--map <file>        Map file in the data/goal folder (optional)
--goal <file>       File in the data/map folder containing start and end  
                    coordinates (optional)
--bias              Add 5% bias to the tree growing (optional)
```

## Loading maps

Custom map and goal files should be put in the `data` folder. They can be loaded by using the
`--map` and `--goal` params and specifying the name of the files.

## Results

Images for trials with varying parameters, along with a video can be found in the `results` folder.

## Files

1. `line.py` contains a function such that given a start and end point, calculate
the point at distance x from the start point.

2. `Map.py` draws the map and the obstacles.

3. `Obstacle.py` defines vertices for an obstacle and contains collision detection methods.

4. `Nearest.py` contains a nearest neighbors implementation.

5. `TreeMap.py` contains the data structure holding the RRT.

6. `map_creator.py` provides an interface to create a new map with obstacles (for testing).
