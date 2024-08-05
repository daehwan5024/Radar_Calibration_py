from NLOS import *

def check_safe(distMeasured, posCal):
    los_l = {}
    for i in range(distMeasured.shape[0]):
        known = 0
        for j in range(distMeasured.shape[1]):
            if not(np.isnan(distMeasured[i, j])):
                known += 1
        los_l[i] = known
    
    # Manually add noise
    distance_modify = np.array(distMeasured)

    for i in range(distance_modify.shape[0]):
        for j in range(distance_modify.shape[1]):
            distance_modify[i, j] = distMeasured[i, j] + np.random.normal(0, 1/30)
            distance_modify[j, i] = distance_modify[i, j]
    
    err = difference(calibrationTriangleSize(distance_modify, distance_modify.shape[0]), posCal)
    return err


if __name__ == '__main__':
    try:
        while True:
            posAbsolute, distMeasured, tags = generate()
            
            st = time.time()
            posCal = calibrationTriangleSize(distMeasured, 16)
            err = difference(posCal, posAbsolute)
            # avg = 0
            # for __ in range(5):
            #     ret = check_safe(distMeasured, posCal)
            #     avg += ret[0]
            # print(avg/5)
            # print(err)
            # print()
            print("===== %s seconds ====="%(time.time() - st))
            
            # plot(posAbsolute, posCal, distMeasured, err, tags)
            data = {'posAbsolute':posAbsolute, 'distMeasured':distMeasured, 'posCal':posCal, 'err':err}
            file_name = "Data/"+((time.ctime().replace(":", "_").replace(" ", "_"))+(".mat"))[4:]
            savemat(file_name, data)
            
            print()
    except KeyboardInterrupt:
        print()
        pass
