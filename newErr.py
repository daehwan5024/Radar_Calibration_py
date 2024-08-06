from NLOS2 import *
import os
from scipy.io import loadmat

if __name__ == "__main__":
    directory_str = "Data/"
    directory = os.fsencode(directory_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mat"):
            data = loadmat(os.path.join(directory_str, filename))
            posAbsolute = data['posAbsolute'];  distMeasured = data['distMeasured']; posCal = data['posCal']
            print(filename)
            print(data['err'])
