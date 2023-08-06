#import os
#import sys
import numpy as np
#import pandas as pd
#from scipy.interpolate import splev, splrep
#from scipy import signal
#from scipy import fftpack
#import functools
import inspect
from .CoreProcessor import *
from .DeviceDefault import CoreDevice
from .ModelDefault import CoreModel
from .MarkerDefault import CoreMarker


class CoreMain(Values,CoreDevice,CoreModel,CoreMarker):
	"""Summary line.
	The CoreMain class gets the data measured by the 3D motion
	analysis device VICON.
	The keywords of the CoreMain class are as follows;
		1. Easily
		2. Quickly
		3. High expandability
	This class is supposed to use data measured using trigger.
	If there is trigeer data, div type method can be used,
	and it is possible to easily obtain multiple trials
	from a single measurement data.

	Parameters
	----------
	data : Composite type
		This data is made by preprocessing module.
	systemsettings : pkl file
	anallysissettings : pkl file

	Returns
	-------
	CoreMain instance
		This instance has many very useful methods.
		Please confirm from the following HP for details.
		'https://sites.google.com/view/pythonforeveryone/python-for-evryone'
	"""
	def __init__(self, data, **kwargs):
		if "cfg" in kwargs.keys():
			super().__init__(data, cfg=kwargs["cfg"])
		else:
			super().__init__(data)


	def getmethod(self):
		"""Summary line.
		Search for a method.

		Parameters
		----------
		None

		Returns
		-------
		list
		All methods of the class.
		"""
		method = []
		for i in inspect.getmembers(self,inspect.ismethod):
			method.append(i[0])
		method.remove("__init__")
		return method


	def ismethod(self, name):
		"""Summary line.
		Search for a method.

		Parameters
		----------
		name : str
			Method name to search.

		Returns
		-------
		list
			all methods including name.
		"""
		if not name:
			return self.getmethod()
		else:
			method = self.getmethod()
			findedmethod = [i for i in method if name[0] in i]
			return findedmethod

	def getinstancedata(self):
		pkl = {}
		pkl["device"] = [self._device, self.deviceheader]
		pkl["model"] = [self._model, self.modelheader]
		pkl["marker"] = [self._marker, self.mkheader]
		pkl["spep"] = self._spep
		pkl["MMT"] = self._mvc
		pkl["rawMMT"] = self._MMTraw
		pkl["ID"] = self._ID
		pkl["EMG_name"] = self._emg_name
		return pkl

	def getSegmentLength_(self, name):
		modellist = {
			"foot" : ["toe", "AJC"],
			"tibia" : ["AJC", "KJC"],
			"femur" : ["KJC", "HJC"],
			"pelvis" : ["RHJC", "LHJC"],
			"radius" : ["WJC", "EJC"],
			"humerus" : ["SJC", "EJC"],
			"thorax":{
				"thorax":["C7", "T10", "CLAV", "STRN"],
				"hip":["RHJC", "LHJC"]
				}
			}
		if name[0] == "R":
			name = name[1:]
			if name == "foot":
				length = np.linalg.norm(self.getMarker("R"+modellist[name][0]) - self.getJointCenter("R"+modellist[name][1]), axis=1).mean()
			else:
				length = np.linalg.norm(self.getJointCenter("R"+modellist[name][0]) - self.getJointCenter("R"+modellist[name][1]), axis=1).mean()
		elif name[0] == "L":
			name = name[1:]
			if name == "foot":
				length =np.linalg.norm(self.getMarker("L"+modellist[name][0]) - self.getJointCenter("L"+modellist[name][1]), axis=1).mean()
			else:
				length = np.linalg.norm(self.getJointCenter("L"+modellist[name][0]) - self.getJointCenter("L"+modellist[name][1]), axis=1).mean()
		elif name[0] == "p":
			length = np.linalg.norm(self.getJointCenter(modellist[name][0]) - self.getJointCenter(modellist[name][1]), axis=1).mean()
		elif name[0] == "t":
			thoraxMKs = self.getMarker(modellist["thorax"]["thorax"])
			vec2x_axis = (thoraxMKs.CLAV + thoraxMKs.STRN +thoraxMKs.T10 - thoraxMKs.C7)*0.5
			unit_vector = vec2x_axis / np.array([np.linalg.norm(vec2x_axis,axis=1)]*3).T
			offsetC7 = thoraxMKs.C7 + 0.65*unit_vector

			HipJoint, z_axis = self.getJointCenter(modellist["thorax"]["hip"]), np.array([0,0,1])
			length = np.linalg.norm(HipJoint.RHJC - HipJoint.LHJC,axis=1) * 0.828
			L5 = 0.5*(HipJoint.RHJC + HipJoint.LHJC) + np.array([length]*3).T * z_axis
			
			length = np.linalg.norm(offsetC7 - L5, axis=1).mean()
		return length

	def getSegmentLength(self, unit="m"):
		namelist = ["Rfoot","Lfoot","Rtibia","Ltibia","Rfemur","Lfemur","pelvis","Rradius","Lradius","Rhumerus","Lhumerus","thorax"]
		dic = {}
		for i in namelist:
			if unit == "m":
				dic[i] = self.getSegmentLength_(i)*0.001
			elif unit == "mm":
				dic[i] = self.getSegmentLength_(i)
		return dic

	def getSegmentCOMLength(self, unit="m"):
		segmentCOMratio = {
			"Rfoot":0.5,
			"Lfoot":0.5,
			"Rtibia":0.567,
			"Ltibia":0.567,
			"Rfemur":0.567,
			"Lfemur":0.567,
			"pelvis":0.925,
			"Rradius":0.57,
			"Lradius":0.57,
			"Rhumerus":0.564,
			"Lhumerus":0.564,
			"thorax":0.63
		}
		
		head = self.getheadCOMlength(unit=unit)
		segment_length = self.getSegmentLength(unit=unit)
		COMlength = np.array(list(segment_length.values())) * np.array(list(segmentCOMratio.values()))
		dic = dict(zip(segmentCOMratio.keys(), COMlength))
		dic["head"] = head
		return dic

	def getbodymass(self, weight):
		bodymassratio =    {
									"pelvis":0.142,
									"femur":0.1*2,
									"tibia":0.0465*2,
									"foot":0.0145*2,
									"humerus":0.028*2,
									"radius":0.016*2,
									"hand":0.006*2,
									"thorax":0.355,
									"head":0.081
									}
		m = np.array(list(bodymassratio.values()))*weight
		return dict(zip(bodymassratio.keys(), m))

	@cvt_HumoArray(argsType="general")
	def getJointCenter2(self, name):
		def calcjointcenter(name):
			if name == "neck":
				thoraxMKs = self.getMarker(["C7", "T10", "CLAV", "STRN"])
				vec2x_axis = (thoraxMKs.CLAV + thoraxMKs.STRN +thoraxMKs.T10 - thoraxMKs.C7)*0.5
				unit_vector = vec2x_axis / np.array([np.linalg.norm(vec2x_axis,axis=1)]*3).T
				offsetC7 = thoraxMKs.C7 + 0.65*unit_vector
				return offsetC7
			elif name == "L5":
				HipJoint, z_axis = self.getJointCenter(["RHJC", "LHJC"]), np.array([0,0,1])
				length = np.linalg.norm(HipJoint.RHJC - HipJoint.LHJC,axis=1) * 0.828
				L5 = 0.5*(HipJoint.RHJC + HipJoint.LHJC) + np.array([length]*3).T * z_axis
				return L5
		
		if type(name) == list:
			return np.array([calcjointcenter(i) for i in name])
		else:
			return calcjointcenter(name)

	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divJointCenter2(self, name, step=None):
		return self.getJointCenter2(name)

	@cvt_HumoArray(argsType="general")
	def getTibiaAngle(self, side , unit="degree"):
		jc = self.getJointCenter([side+"KJC", side+"AJC"]).yz
		sign = np.sign(jc[0][:,0] - jc[1][:,0])
		v = jc[0] - jc[1]
		z = np.array([0,1]*jc[0][:,0].size).reshape(-1,2)
		Lv, Lz =np.linalg.norm(v, axis=1), np.linalg.norm(z, axis=1)
		innerdot = (v*z).sum(axis=1)
		c = innerdot / (Lz * Lv)
		if unit == "degree":
			theta = np.rad2deg(np.arccos(c)).reshape(-1,1)
		elif unit == "radian":
			theta = np.arccos(c).reshape(-1,1)
		res = np.array([0,0]*c.size).reshape(-1,2)
		return np.hstack((theta,res)) * sign.reshape(-1,1)


	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divTibiaAngle(self, side, step=None, unit="degree"):
		return self.getTibiaAngle(side, unit)


	@cvt_HumoArray(argsType="general")
	@differentation(difforder="1st")
	def getTibiaAngleVel(self, side , unit="degree"):
		jc = self._getJointCenter([side+"KJC", side+"AJC"]).yz
		sign = np.sign(jc[0][:,0] - jc[1][:,0])
		v = jc[0] - jc[1]
		z = np.array([0,1]*jc[0][:,0].size).reshape(-1,2)
		Lv, Lz =np.linalg.norm(v, axis=1), np.linalg.norm(z, axis=1)
		innerdot = (v*z).sum(axis=1)
		c = innerdot/ (Lz * Lv)
		if unit == "degree":
			theta = np.rad2deg(np.arccos(c)).reshape(-1,1)
		elif unit == "radian":
			theta = np.arccos(c).reshape(-1,1)
		res = np.array([0,0]*c.size).reshape(-1,2)
		return np.hstack((theta, res)) * sign.reshape(-1,1)

	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divTibiaAngleVel(self, side, step=None, unit="degree"):
		return self.getTibiaAngleVel(side, unit)

	@cvt_HumoArray(argsType="general")
	@differentation(difforder="2nd")
	def getTibiaAngleAcc(self, side , unit="degree"):
		jc = self._getJointCenter([side+"KJC", side+"AJC"]).yz
		sign = np.sign(jc[0][:,0] - jc[1][:,0])
		v = jc[0] - jc[1]
		z = np.array([0,1]*jc[0][:,0].size).reshape(-1,2)
		Lv, Lz =np.linalg.norm(v, axis=1), np.linalg.norm(z, axis=1)
		innerdot = (v*z).sum(axis=1)
		c = innerdot / (Lz * Lv)
		if unit == "degree":
			theta = np.rad2deg(np.arccos(c)).reshape(-1,1)
		elif unit == "radian":
			theta = np.arccos(c).reshape(-1,1)
		res = np.array([0,0]*c.size).reshape(-1,2)
		return np.hstack((theta, res)) * sign.reshape(-1,1)

	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divTibiaAngleAcc(self, side, step=None, unit="degree"):
		return self.getTibiaAngleAcc(side, unit)


	def getheadCOMpos(self):
		front = self.getMarker(["LFHD", "RFHD"])
		back = self.getMarker(["LBHD", "RBHD"])
		vector = (back.LBHD + back.RBHD - front.LFHD - front.RFHD)/2
		vector_ = np.linalg.norm(vector,axis=1)
		nvec  = vector / np.array([vector_]*3).T
		headlength = vector_*0.52
		headCOMpos = (front.LFHD + front.RFHD)/2 + nvec*np.array([headlength]*3).T
		return headCOMpos

	def getheadCOMlength(self, unit="m"):
		headcom = self.getheadCOMpos()
		C7 = self.getJointCenter2("neck")
		if unit == "m":
			return np.linalg.norm(headcom - C7, axis=1).mean()*0.001
		elif unit == "mm":
			return np.linalg.norm(headcom - C7, axis=1).mean()

