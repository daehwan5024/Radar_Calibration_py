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
    # noise_added = 0
    # for w in sorted(los_l, key=los_l.get, reverse=True):
    #     if noise_added >= 4:
    #         break
    #     noise_added += 1
    #     for j in range(distance_modify.shape[1]):
    #         if w != j:
    #             add = 1
    #             if np.random.rand() < 0.5:
    #                 add = -1
    #             distance_modify[w, j] += 0.03*add
    #             distance_modify[j, w] += 0.03*add

    for i in range(distance_modify.shape[0]):
        for j in range(distance_modify.shape[1]):
            distance_modify[i, j] = distMeasured[i, j] + np.random.normal(0, 1/30)
            distance_modify[j, i] = distance_modify[i, j]
    
    err = difference(calibrationTriangleSize(distance_modify, distance_modify.shape[0]), posCal)
    print("Manualy added noise", err)


if __name__ == '__main__':
    try:
        while True:
            posAbsolute, distMeasured, tags = generate()

            posCal = calibrationTriangleSize(distMeasured, 16)
            err = difference(posCal, posAbsolute)
            check_safe(distMeasured, posCal)
            check_safe(distMeasured, posCal)
            check_safe(distMeasured, posCal)
            print(err)
            data = {'posAbsolute':posAbsolute, 'distMeasured':distMeasured, 'posCal':posCal, 'err':err}
            file_name = "Data/"+((time.ctime().replace(":", "_").replace(" ", "_"))+(".mat"))[4:]
            savemat(file_name, data)
            
            print()
    except KeyboardInterrupt:
        print()
        pass
