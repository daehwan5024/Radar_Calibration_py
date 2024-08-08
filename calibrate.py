from calibration import calibrationTriangleSize
from simulation import radarData2
from evaluation import difference

num_top, num_bottom, posAbsolute, distAbsolute, distMeasured = radarData2()
posCalibrated = calibrationTriangleSize(distMeasured, num_top+num_bottom)
print(difference(posAbsolute, posCalibrated))
