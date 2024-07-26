from util import calibrationTriangleSize
import time
import numpy as np
from scipy.io import loadmat

data = loadmat('C:\\Users\\smile\\Radar_Calibration\\test.mat')
st = time.time()
print(data)
posCalibrated = calibrationTriangleSize(data['distMeasured'], data['num_radar'][0][0]+data['num_bottom'][0][0])
print("--- %s seconds ---" % (time.time() - st))
print(posCalibrated)