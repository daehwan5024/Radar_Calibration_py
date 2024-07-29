import numpy as np
from util import pairwiseDist
np.seterr(divide='ignore', invalid='ignore')
num_radar = 5
a = np.array([[1, 1, 1, 1, 1], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
b = pairwiseDist(a)
c = pairwiseDist(a)
for i in range(5):
    for j in range(i):
        if i==j:
            continue
        c[i, j] = b[i, j] + 0.1
        c[j, i] = c[i, j]
const = (c-b)/b

lx = np.reshape([const[i, j]*(a[k,i]-a[k,j]) for k in range(3) for i in range(5) for j in range(5)], (3,5,5))
loss = np.zeros((3, num_radar))
for i in range(num_radar):
    loss_t = np.zeros(3)
    for j in range(num_radar):
        if i == j:
            continue
        if np.isnan(c[i, j]):
            continue
        dist_ij = np.linalg.norm(a[:,i] - a[:,j])
        const = (dist_ij - c[i, j])/dist_ij
        loss_t = loss_t + 2*const*(a[:,i] - a[:,j])
    loss[:,i] = loss_t
print(loss)
print(np.nansum(lx, axis=1))

