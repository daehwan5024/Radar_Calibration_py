from util import getInsertOrder
import time
import numpy as np
from scipy.io import loadmat

data = loadmat('C:\\Users\\smile\\Radar_Calibration\\test.mat')
print(data)
st = time.time()
print("--- %s seconds ---" % (time.time() - st))