# Radar Auto Calibration

Simillar to [Radar_Calibration](https://github.com/daehwan5024/Radar_Calibration)\
Instead of using matlab, it uses python

## How to use

`calibrate.py` will load data from `test.mat` and run calibration

`util.py` holds the functions that calibrates the given data.\
Function `calibrationTriangleSize` has `measured distance` and `number of radars` as input\
return value is the calibrated position of radars
