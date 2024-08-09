# Radar Auto Calibration

`numpy`, `matplotlib` is required

## `calibration.py` essential functions for calibration

`pairwiseDist`: computes pairwise distance for given position

`getBetter`: returns value that better fits the meausred data

`getTriangle`: returns 3 point of triangle having specific distance

`getTriangleList`: list of all possible triangles and their area

`getTrilateration`: result of trilateration using 3 points

`calibrationTriangleSize`: takes `Measured distance` and `num_radar` as input and returns calibrated position

`gradient.so`: shared library for gradient descent. Can be used at linux. If using at other OS, recompile `gradient.c` for that specific OS

## `evaluation.py` : evaluating calibrated result

`getTransform`: returns Rotation and Translation matrix that best matches `input1` to `input2`, [related infromation](https://taeyoung96.github.io/slam/SLAM_03_1/)

`difference`: using `getTransform` return mean difference of each point for the given data

## `simulation.py` : used for simulating a specific condition

`addNoise`: add noise to the input

`addNoise2`: add noise to input, except distance between tags

`radarData`: create random data assuming that radars are spread in a room of size 20x20

`radarData2`: create random data assuming that radars are spread at wall of a 20x20 room

## `NLOS.py` : simulates situation with 2 rooms

`generate`: creates random data that satisfy the given condition

`noise`: add noise for this specific situation

## `E3.py` : simulates blockages at E3-2 Lobby

simulates blockage by ceiling and pillars\
Assume that each surface is rectangle with sides parallel to x, y or z axis

## `Calibrate.py`

Simple example of data generation and calibration
