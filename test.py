import ctypes
import pathlib
lib_path = pathlib.Path("build/libscale.dll")
dll = ctypes.CDLL(str(lib_path.resolve()))
print(dll.sq(100))