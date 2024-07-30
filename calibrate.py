from util import calibrationTriangleSize
from scipy.io import loadmat
import time

data = loadmat('./test.mat')
print(data['num_radar'][0][0]+data['num_bottom'][0][0])

start_time = time.time()
posCalibrated = calibrationTriangleSize(data['distMeasured'], data['num_radar'][0][0]+data['num_bottom'][0][0])
print("--- %s seconds ---" % (time.time() - start_time))
print(posCalibrated)