import numpy as np
import os

class Prepack:
	
	def __init__(self, path='', duration=10):
		if not isinstance(duration, (float, int)):
			raise TypeError("Sample duration must be a number.")
		
		self.sourcepath = path
		self.duration = duration
		
		self.source = np.full((1, 3), None)
		self.channels = 1
		self.points = 1
	
		self.filename = os.path.split(path)[1]
	
	def set_channels(self, channels_num):
		self.channels = channels_num
	
	def set_points(self, points_num):
		self.points = points_num
	
	def set_source(self, array):
		self.source = array
