from util import calibrationTriangleSize
from util_t import *
from scipy.io import loadmat
import time

data = loadmat('./test.mat')
print(data['num_radar'][0][0]+data['num_bottom'][0][0])

st = time.time()
posCalibrated = calibrationTriangleSize(data['distMeasured'], data['num_radar'][0][0]+data['num_bottom'][0][0])
print("--- %s seconds ---" % (time.time() - st))
print(difference(data['posAbsolute'], posCalibrated))