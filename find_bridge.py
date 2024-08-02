from NLOS import *

posAbsolute, distMeasured, tags = generate()
np.set_printoptions(edgeitems=30, linewidth=100000)
connected = np.invert(np.isnan(distMeasured))
ans = {}

for i in range(connected.shape[1]):
    for j in range(i):
        num_tri = 0
        for k in range(connected.shape[1]):
            if i==k or j==k:
                continue
            if connected[i, j] and connected[j, k] and connected[k, i]:
                num_tri += 1
        ans[(j, i)] = num_tri
for w in sorted(ans, key=ans.get):
    print('(%2d, %2d)'%(w[0], w[1]), ans[w])
plot(posAbsolute, None, distMeasured, None, tags)
