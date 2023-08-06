import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools


"""
Dividing data with trigger.
"""
def dividingData(dimension):
	def _dividingData(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			sp, ep = args[0]._spep[0][0], args[0]._spep[0][1]
			if not kwargs:
				pass
			else:
				first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
				sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
			dividedData = []
			if dimension == 3:
				try:
					if type(args[1]) == list:
						for i in data:
							dividingData_ = []
							for j in range(len(sp)):
								dividingData_.append(np.array(i[sp[j]:ep[j],:]))
							dividedData.append(dividingData_)
					else:
						for i in range(len(sp)):
							dividedData.append(np.array(data[sp[i]:ep[i],:]))
				except IndexError: # for COM, COM_floor. These don't need argments.
					for i in range(len(sp)):
						dividedData.append(np.array(data[sp[i]:ep[i],:]))
			elif dimension == 1:
				if type(args[1]) == list:
					for i in data:
						dividingData_ = []
						for j in range(len(sp)):
							dividingData_.append(np.array(i[sp[i]:ep[i]]))
						dividedData.append(dividingData_)
				else:
					for i in range(len(sp)):
						dividedData.append(np.array(data[sp[i]:ep[i]]))
			return np.array(dividedData)
		return wrapper
	return _dividingData


def dividingDeviceData(dimension):
	def _dividingData(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			sp, ep = args[0]._spep[1][0], args[0]._spep[1][1]
			if not kwargs:
				pass
			else:
				first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
				sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
			dividedData = []
			if dimension == 3:
				if type(args[1]) == list:
					for i in data:
						dividedData_ = []
						for s,e in zip(sp, ep):
							dividedData_.append(np.array(i[s:e,:]))
						dividedData.append(dividedData_)
					return np.array(dividedData)
				else:
					for i in range(len(sp)):
						dividedData.append(np.array(data[sp[i]:ep[i],:]))
			elif dimension == 1:
				if type(args[1]) == list:
					for i in data:
						dividedData_ = []
						for s, e in zip(sp, ep):
							dividedData_.append(np.array(i[s:e]))
						dividedData.append(dividedData_)
				else:
					for i in range(len(sp)):
						dividedData.append(np.array(data[sp[i]:ep[i]]))
			return np.array(dividedData)
		return wrapper
	return _dividingData


def dividingDeviceData2(dimension):
	def _dividingData(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			#print(data)
			sp, ep = args[0]._spep[1][0], args[0]._spep[1][1]
			dividedData = []
			if dimension == 3:
				for i in range(len(sp)):
					dividedData.append(data[sp[i]:ep[i],:])
			elif dimension == 1:
				for i in range(len(sp)):
					dividedData.append(data[sp[i]:ep[i]])
			return dividedData
		return wrapper
	return _dividingData




