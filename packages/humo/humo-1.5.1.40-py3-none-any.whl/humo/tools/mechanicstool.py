import numpy as np

def radian(data):
    keys, values = data._asdict().keys(), data._asdict().values()
    dic = {}
    for i, j in zip(keys, values):
        dic[i] = np.radians(j)
    return dic

def radianvel(data):
    keys, values = data._asdict().keys(), data._asdict().values()
    dic = {}
    for i, j in zip(keys, values):
        dic[i] = 180*j/np.pi
    return dic
