import joblib
import pickle

import numpy as np
import matplotlib.pyplot as plt

import cv2
from skimage.transform import radon, rescale
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random



class VCP(object):
    def __init__(self, filename):
        self.filename = filename
        self.video = cv2.VideoCapture(filename)
        self.read_check = self.video.read()[0]
        if self.read_check == True:
            pass
        else:# ここは例外を吐くようにする
            print("="*30)
            print("Video did not be read.")
            print("Chekc path to video data.")
            print("="*30)
        self.count = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.H1 = 48
        self.H2 = 320
        self.V1 = 230
        self.V2 = 410
        
        
    def check_crop_area(self, *area,  dvalues=True):
        if dvalues == True:
            plt.figure(figsize=(10,10))
            plt.imshow(self.video.read()[1])
            plt.axhline(self.H1, color="g")
            plt.axhline(self.H2, color="r")
            plt.axvline(self.V1, color="c")
            plt.axvline(self.V2, color="y")
        else:
            plt.figure(figsize=(10,10))
            plt.imshow(self.video.read()[1])
            plt.axhline(area[0], color="g")
            plt.axhline(area[1], color="r")
            plt.axvline(area[2], color="c")
            plt.axvline(area[3], color="y")
        
    def set_crop_area(self, h1, h2, v1, v2):
        self.H1 = h1
        self.H2 = h2
        self.V1 = v1
        self.V2 = v2
        print("The crop area has been set successfully.")


    def crop_area(self):
        vdata = cv2.VideoCapture(self.filename)
        crop_data = []
        for i in range(int(self.count)):
            b = vdata.read()[1]
            b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
            crop_data.append(b[self.H1:self.H2,self.V1:self.V2])
        self.__crop_data = np.array(crop_data)

    
    def substract_crop_area(self):
        substract_crop_data = []
        for i in self.__crop_data:
            v = (i - i.mean())
            #v = np.where(v < 0, 0, v).astype("uint8")
            v = np.where(v < 0, 0, v)
            substract_crop_data.append(v)
        self.__substract_crop_data = np.array(substract_crop_data)
        
    def radonn_transform(self, workers = -2):
        def radonn_proc(img):
            rimg =  radon(img, circle=False, preserve_range=False)
            #return rimg.astype("uint8")
            return rimg
        rvideo = joblib.Parallel(n_jobs=workers, verbose=2)([joblib.delayed(radonn_proc)(i) for i in self.__substract_crop_data])
        self.__radonn_img = np.array(rvideo)
        
    def partial_differential(self, kernel_coefficient=0.25):
        kernel_a = kernel_coefficient * np.array([
            [-1,-2,-1],
            [0,0,0],
            [1,1,1]
        ])
        kernel_b = kernel_coefficient * np.array([
            [1,2,1],
            [0,0,0],
            [-1,-2,-1]
        ])
        self.__G1 = np.array([cv2.filter2D(i, -1, kernel_a) for i in self.__radonn_img])
        self.__G2 = np.array([cv2.filter2D(i, -1, kernel_b) for i in self.__radonn_img])

    def create_aes(self, password, iv):
        sha = SHA256.new()
        sha.update(password.encode())
        key = sha.digest()
        return AES.new(key, AES.MODE_CFB, iv)
    
    def encrypt(self, data):
        iv = Random.new().read(AES.block_size)
        return iv + self.create_aes("test_passward", iv).encrypt(data)        


    def video_conversion(self, workers = -2, kernel_coefficient = 0.25):
        self.crop_area()
        self.substract_crop_area()
        self.radonn_transform(workers=workers)
        self.partial_differential(kernel_coefficient=kernel_coefficient)
        
    def save_data(self, filename, workers=-2, kernel_coefficient=0.25):
        self.video_conversion(workers, kernel_coefficient)
        pdata = {
            "gsv" : self.encrypt(self.__crop_data.tobytes()),
            "gsv_shape" : self.__crop_data[0].shape,
            "gsv_dtype" : str(self.__crop_data.dtype),
            "gsvave" : self.encrypt(self.__substract_crop_data.tobytes()),
            "gsvave_shape" : self.__substract_crop_data[0].shape,
            "gsvave_dtype" : str(self.__substract_crop_data.dtype),
            "radonn" : self.encrypt(self.__radonn_img.tobytes()),
            "radonn_shape" : self.__radonn_img[0].shape,
            "radonn_dtype" : str(self.__radonn_img.dtype),
            "G1" : self.encrypt(self.__G1.tobytes()),
            "G1_shape" : self.__G1[0].shape,
            "G1_dtype" : str(self.__G1.dtype),
            "G2" : self.encrypt(self.__G2.tobytes()),
            "G2_shape" : self.__G2[0].shape,
            "G2_dtype" : str(self.__G2.dtype)
        }
        with open(filename+".bin", mode="wb") as f:
            pickle.dump(pdata, f)
            
    def save_movie(self, filename, frame_rate=30.0):
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # crop動画の保存
        size = self.crop_data[0].shape[::-1]
        writer_crop = cv2.VideoWriter(filename + "_crop.mp4", fmt, frame_rate, size, isColor=False)
        for i in range(int(self.count)):
            writer_crop.write(self.crop_data[i])
        writer_crop.release()
        
        # substract動画の保存
        size = self.substract_crop_data[0].shape[::-1]
        writer_substract = cv2.VideoWriter(filename + "_substract.mp4", fmt, frame_rate, size, isColor=False)
        for i in range(int(self.count)):
            writer_substract.write(self.substract_crop_data[i])
        writer_substract.release()
        
        # radonn動画の保存
        size = self.radonn_img[0].shape[::-1]
        writer_radonn = cv2.VideoWriter(filename + "_radonn.mp4", fmt, frame_rate, size, isColor=False)
        for i in range(int(self.count)):
            writer_radonn.write(self.radonn_img[i])
        writer_radonn.release()
            
        # G1, G2動画の保存
        size = self.G1[0].shape[::-1]
        writer_G1 = cv2.VideoWriter(filename + "_G1.mp4", fmt, frame_rate, size, isColor=False)
        writer_G2 = cv2.VideoWriter(filename + "_G2.mp4", fmt, frame_rate, size, isColor=False)
        for i in range(int(self.count)):
            writer_G1.write(self.G1[i])
            writer_G2.write(self.G2[i])
        writer_G1.release()
        writer_G2.release()
        
        
        
            

test = VCP(r"testdata/testdata.mp4")