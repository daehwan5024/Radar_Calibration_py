import ctypes
import numpy as np

libmatmult = ctypes.CDLL("./add.so")
a = np.array([[1,2],[3,4]], dtype=np.float64)
ND_POINTER_1 = np.ctypeslib.ndpointer(dtype=np.float64, 
                                      ndim=2,
                                      flags="C")
ND_POINTER_2 = np.ctypeslib.ndpointer(dtype=np.float64, 
                                    ndim=2,
                                    flags="C")
libmatmult.sum.argtypes = [ctypes.c_int, ND_POINTER_2]
# print("-->", ctypes.c_size_t)
libmatmult.sum(2, a)
