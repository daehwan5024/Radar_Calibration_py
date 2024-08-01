from util_t import *
import time
num_top, num_bottom, posAbsolute, distAbsolute, distMeasured = radarData2(10, 3, 4)
# for i in range(num_bottom+num_top):
#     for j in range(num_bottom+num_top):
#         if i>num_bottom and j> num_bottom and distMeasured[i, j] >= 20:
#             distMeasured[i, j] = np.nan

st = time.time()
posCal = calibrationTriangleSize(distMeasured, num_top+num_bottom)
print("--- %s seconds ---" % (time.time() - st))

err = difference(posCal, posAbsolute)
print(posCal)
print(err)