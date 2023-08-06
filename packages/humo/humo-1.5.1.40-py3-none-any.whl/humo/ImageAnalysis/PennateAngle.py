import joblib
import numpy as np
import matplotlib.pyplot as plt
import pickle
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from sklearn.mixture import GaussianMixture
from .utilitymod import TRC
from .utilitymod import FiberLines
from .utilitymod import Pixels
from .utilitymod import Lines
from .utilitymod import Particle
from .utilitymod import PMA
from .utilitymod import line
from typing import NamedTuple


class PennateAngle(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.gsv = None
        self.gsvave = None
        self.radonn = None
        self.G1 = None
        self.G2 = None
        self.ratio = 0.2
        self.lowerlimit = 30
        self.upperlimit = 150
        self.set_data_simple()
        self.set_data()

    def read_data(self):
        with open(self.filepath, "rb") as f:
            a =  pickle.load(f)
        return a

    def set_ratio(self, ratio):
        self.ratio = ratio
        print("The ratio has been set successfully.")

    def set_limit(self, lowerlimit, upperlimit):
        self.lowerlimit = lowerlimit
        self.upperlimit = upperlimit
        print("The limit values have been set successfully.")

    def create_aes(self, password, iv):
        sha = SHA256.new()
        sha.update(password.encode())
        key = sha.digest()
        return AES.new(key, AES.MODE_CFB, iv)

    def decrypt(self, data, shape, dtype):
        iv, cipher = data[:AES.block_size], data[AES.block_size:]
        res = self.create_aes("test_passward", iv).decrypt(cipher)
        return np.frombuffer(res, dtype).reshape(-1, shape[0], shape[1])

    def set_data_simple(self):
        data = self.read_data()
        self.G1 = self.decrypt(data["G1"], data["G1_shape"], data["G1_dtype"])
        self.G2 = self.decrypt(data["G2"], data["G2_shape"], data["G2_dtype"])
        self.fcount = self.G1.shape[0]
        self.shape2 = [self.G1.shape[1], self.G1.shape[2]]
        self.axlim2 = [(self.shape2[0], 0), (0, self.shape2[1])]
        del data

    def set_data(self):
        data = self.read_data()
        self.gsv = self.decrypt(data["gsv"], data["gsv_shape"], data["gsv_dtype"])
        self.gsvave = self.decrypt(data["gsvave"], data["gsvave_shape"], data["gsvave_dtype"])
        self.radonn = self.decrypt(data["radonn"], data["radonn_shape"], data["radonn_dtype"])
        self.shape1 = [self.gsv.shape[1], self.gsv.shape[2]]
        self.axlim1 = [(self.shape1[0], 0), (0, self.shape1[1])]
        del data



    def getPixels(self, frame):
        val = sorted(self.G1[frame].ravel())[-int(self.G1[frame].size * self.ratio * 0.01)::]
        y, x = np.where(self.G1[frame] >= val[0])
        return x, y

    def getPixelsGMM(self, *frame):
        if frame == ():
            sa, pm, da = [], [], []
            for f in range(self.fcount):
                theta, rho = self.getPixels(f)
                _upperlimit= list(np.where(theta > self.upperlimit)[0])
                _lowerlimit = list(np.where(theta < self.lowerlimit)[0])
                _upperlimit.extend(_lowerlimit)
                theta = np.delete(theta, _upperlimit)
                rho = np.delete(rho, _upperlimit)
                cdata = np.array([theta, rho]).T
                res = GaussianMixture(n_components=3).fit_predict(cdata)
                sign = np.array([cdata[res==i].mean(axis=0)[1] for i in range(3)])
                res = [TRC(cdata[res==np.argsort(sign)[i]]) for i in range(3)]
                sa.append(res[0].theta_)
                pm.append(res[1].theta_)
                da.append(res[2].theta_)
                result = PMA(line( -np.array(da)), line(-np.array(pm)),line(-np.array(sa)))
            return result
        else:
            frame = frame[0]
            theta, rho = self.getPixels(frame)
            _upperlimit= list(np.where(theta > self.upperlimit)[0])
            _lowerlimit = list(np.where(theta < self.lowerlimit)[0])
            _upperlimit.extend(_lowerlimit)
            theta = np.delete(theta, _upperlimit)
            rho = np.delete(rho, _upperlimit)
            cdata = np.array([theta, rho]).T
            res = GaussianMixture(n_components=3).fit_predict(cdata)
            sign = np.array([cdata[res==i].mean(axis=0)[1] for i in range(3)])
            res = [TRC(cdata[res==np.argsort(sign)[i]]) for i in range(3)]
            return Pixels(res[2], res[1], res[0])
    

    #def _getLine(self, frame, fibertype):
    #    val = self.getPixelsGMM(frame)
    #    val = getattr(val, fibertype)
    #    Yshape, Xshape = self.gsv[0].shape

    #    x = np.arange(0, Xshape, 1)
    #    positive_, negative_ = [], []
    #    for i, j in zip(val.theta, val.rho):
    #        tilt = np.radians(90 - i)
    #        if np.radians(90 - i) >= 0:
    #            positive_.append(np.tan(tilt)*(x - Xshape/2) + Yshape/2 - (j - self.G1[0].shape[0]/2))
    #        else:
    #            negative_.append(np.tan(tilt)*(x - Xshape/2) + Yshape/2 - (j - self.G1[0].shape[0]/2))
    #    return Lines(positive_, negative_)

    #def _getLine(self, frame, val):
    #    Yshape, Xshape = self.gsv[0].shape
    #    x = np.arange(0, Xshape, 1)
    #    positive_, negative_ = [], []
    #    for i, j in zip(val.theta, val.rho):
    #        tilt = np.radians(90 - i)
    #        if np.radians(90 - i) >= 0:
    #            positive_.append(np.tan(tilt)*(x - Xshape/2) + Yshape/2 - (j - self.G1[0].shape[0]/2))
    #        else:
    #            negative_.append(np.tan(tilt)*(x - Xshape/2) + Yshape/2 - (j - self.G1[0].shape[0]/2))
    #    return Lines(positive_, negative_)

    def _getLine(self, frame, val):
        Yshape, Xshape = self.gsv[0].shape
        x = np.arange(0, Xshape, 1)
        res = []
        for i, j in zip(val.theta, val.rho):
            tilt = np.radians(90 - i)
            res.append(np.tan(tilt)*(x - Xshape/2) + Yshape/2 - (j - self.G1[0].shape[0]/2))
        return Particle(np.array(res))

    #def _getAverageLine(self, frame, fibertype):
    #    val = self.getPixelsGMM(frame)
    #    val = getattr(val, fibertype)
    #    Yshape, Xshape = self.gsv[0].shape
    #    x = np.arange(0, Xshape, 1)
    #    return np.tan(np.radians(val.theta_))*(x - Xshape/2) + Yshape/2 - (val.rho_ - self.G1[0].shape[0]/2)

    def _getAverageLine(self, frame, val):
        Yshape, Xshape = self.gsv[0].shape
        x = np.arange(0, Xshape, 1)
        res = np.tan(np.radians(val.theta_))*(x - Xshape/2) + Yshape/2 - (val.rho_ - self.G1[0].shape[0]/2)
        return Particle(res)

    #def getFiberLines(self, frame):
    #    a = [self._getLine(frame, i) for i in ["sa", "pm", "da"]]
    #    b = [self._getAverageLine(frame, i) for i in ["sa", "pm", "da"]]
    #    a.extend(b)
    #    return FiberLines(*a)

    def getFiberLines(self, frame):
        temp = self.getPixelsGMM(frame)
        a = [self._getLine(frame, getattr(temp, i)) for i in ["sa", "pm", "da"]]
        b = [self._getAverageLine(frame, getattr(temp, i)) for i in ["sa", "pm", "da"]]
        a.extend(b)
        return FiberLines(*a)



















    def IOI(self, frame, ratio=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]):
        pixels = [self.getPixels(frame, i) for i in ratio]
        plt.figure(figsize=(14,14))
        plt.suptitle(f"Frame : {frame} -> Time : {frame/30:.2f}sec", fontsize=30)

        plt.subplot(2,4,1)
        plt.title("original", fontsize=15)
        plt.imshow(self.gsv[frame], cmap="gray")
        plt.grid(c="c")
        plt.axhline(136, c="r")

        plt.subplot(2,4,5)
        plt.title("substract mean", fontsize=15)
        plt.imshow(self.gsvave[frame], cmap="gray")
        plt.grid(c="c")
        plt.axhline(136, c="r")

        for num, i in enumerate([2,3,4,6,7,8]):
            plt.subplot(2,4,i)
            plt.title(f"top : {ratio[num]}% [ {pixels[num][0].size}/{self.G1[0].size} ]", fontsize=15)
            plt.imshow(self.G1[frame], cmap="gray")
            plt.scatter(pixels[num][0], pixels[num][1], facecolor="None", edgecolor="g", alpha=0.5,s=3)
            plt.grid(c="w")
            plt.axhline(193, c="r")
        plt.tight_layout(rect=[0,0,1,0.98])
        