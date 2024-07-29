from util2 import calibrationTriangleSize
import numpy as np
from scipy.io import loadmat

data = loadmat('C:\\Users\\smile\\Radar_Calibration\\test.mat')

posCalibrated = calibrationTriangleSize(data['distMeasured'], data['num_radar'][0][0]+data['num_bottom'][0][0])

print(posCalibrated)