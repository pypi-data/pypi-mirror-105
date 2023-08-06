import numpy as np
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools



"""
This is a wrapper for performing differential calculations.
The wrapper accepts self and column names,
and outputs the first-order and second-order differentiated data.

When first-order and second-order differentiation, pass 1 or 2 to the difforder in the wrapper.
"""


def differentation(difforder):
    def differentation_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            filtMod = args[0]._ASP["diff_filter"]
            unit = "msec"
            if difforder == "1st":
                if filtMod[0] == "True":
                    if data.ndim == 3:
                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
                        data_diff = []
                        for i in data:
                            data_ = (i[2:] - i[:-2]) / 0.01*2
                            data_diff.append(np.array([signal.filtfilt(b,a,data_[:,axis]) for axis in tuple(np.arange(3))]).T)
                    else:
                        data_diff = (data[2:] - data[:-2]) / 0.01*2
                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
                        data_diff = np.array([signal.filtfilt(b,a,data_diff[:,axis]) for axis in tuple(np.arange(3))]).T
                elif filtMod[0] == "False":
                    if data.ndim == 3:
                        data_diff = []
                        for i in data:
                            data_diff.append((i[2:] - i[:-2]) / 0.01*2)
                    else:
                        data_diff = (i[2:] - i[:-2]) / 0.01*2
            if difforder == "2nd":
                if filtMod[0] == "True":
                    if data.ndim == 3:
                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
                        data_diff = []
                        for i in data:
                            data_ = (i[2:] - i[1:-1]*2 + i[:-2]) / 0.01**2
                            data_diff.append(np.array([signal.filtfilt(b,a,data_[:,axis]) for axis in tuple(np.arange(3))]).T)
                    else:
                        data_diff = (data[2:] - data[1:-1]*2 + data[:-2]) / 0.01**2
                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
                        data_diff = np.array([signal.filtfilt(b,a,data_diff[:,axis]) for axis in tuple(np.arange(3))]).T
                elif filtMod[0] == "False":
                    if data.ndim == 3:
                        data_diff = []
                        for i in data:
                            data_diff((i[2:] - i[1:-1]*2 + i[:-2]) / 0.01**2)
                    else:
                        data_diff = (data[2:] - data[1:-1]*2 + data[:-2]) / 0.01**2
            if unit == "msec":
                return np.array(data_diff) / 10000.0
            elif unit == "sec":
                return np.array(data_diff)
        return wrapper
    return differentation_




