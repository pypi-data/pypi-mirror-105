import numpy as np
from typing import NamedTuple
import matplotlib.pyplot as plt

class TRC(object):
    # theta_rho_converter
    def __init__(self, data):
        self.data = data
        self.theta = data[:,0]
        self.rho = data[:,1]
        self.theta_ = self.weight_theta()
        self.rho_ = self.weight_rho()
    
    def weight_theta(self):
        theta = 90 - self.theta
        a, b = np.unique(theta, return_counts=True)
        return np.average(a, weights=b)
    
    def weight_rho(self):
        a, b = np.unique(self.rho, return_counts=True)
        return np.average(a, weights=b)

class PMA(object):
    def __init__(self, sa, pm, da):
        self.sa = sa
        self.pm = pm
        self.da = da

    def getPMangle(self, **kwargs):
        if kwargs == {}:
            return self.pm - self.da
        else:
            mav = kwargs["mav"]
            a = self.pm - self.da
            a = np.convolve(a, np.ones(mav)/mav, mode="same")
            return a




class Particle(np.ndarray):
    def __new__(cls, array):
        obj = np.asarray(array).view(cls)
        return obj

    def __init__(self, array):
        self.array = array

    def plot(self,  *, c=None, lw=None, ls=None, alpha=None, label=None):
        if self.array.ndim == 1:
            plt.plot(self.array, c=c, lw=lw, ls=ls,alpha=alpha,label=label)

        else:
            x = np.arange(self.array.shape[1])
            for i in np.arange(self.array.shape[0]):
                plt.plot(x, self.array[i,:], c=c, lw=lw, ls=ls,alpha=alpha)


class Lines(NamedTuple):
    positive : list
    negative : list

class FiberLines(NamedTuple):
    sa : list 
    pm : list
    da : list
    sa_ : list
    pm_ : list
    da_ : list


class Pixels(NamedTuple):
    sa : list
    pm : list
    da : list