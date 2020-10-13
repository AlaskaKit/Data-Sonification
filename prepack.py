import numpy as np
import os


class Prepack:
	"""
	Class-container for the parameters used by components of the sonification cycle.
	Re-checks the duration value in constructor.
	Properties:
		self.sourcepath: path to the user's file
		self.duration: duration of the sample in secs
		self.source: an array for user's data and after the converting - for the frequencies.
		self.channels: number of channels (columns for the sonification)
		self.points: number of points (rows or lines for the sonification)
		self.filename: name of the user's file.
		
	Has three setters for the overwriting channels, points and source.
	"""
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
