from util import calibrationTriangleSize
from util_t import radarData2, difference
from scipy.io import loadmat
import time

num_top, num_bottom, posAbsolute, distAbsolute, distMeasured = radarData2()


posCalibrated = calibrationTriangleSize(distMeasured, num_top+num_bottom)

print(difference(posAbsolute, posCalibrated))
