import numpy as np


class FqConverter:
	def __init__(self, num_container, num_channels, num_points):
		self.largest = None
		self.smallest = None
		self.source = num_container
		self.fqs = np.full((num_points, num_channels), 0, dtype=float)
		
		for x in range(num_channels):
			for y in range(num_points):
				if self.largest is None:
					self.largest = num_container[y][x]
				elif num_container[y][x] is None:
					continue
				elif num_container[y][x] > self.largest:
					self.largest = num_container[y][x]
				else:
					continue
		
		for x in range(num_channels):
			for y in range(num_points):
				if self.smallest is None:
					self.smallest = num_container[y][x]
				elif num_container[y][x] is None:
					continue
				elif num_container[y][x] < self.smallest:
					self.smallest = num_container[y][x]
				else:
					continue
		
		self.gap = self.largest - self.smallest
		
	def __convert(self, point):
		if point is None:
			return
		else:
			ratio = (point - self.smallest) / self.gap
			fq = 220 * 2 ** (2* ratio)
		return fq
		
	def get_fqs(self):
		vect_converter = np.vectorize(self.__convert)
		self.fqs = vect_converter(self.source)
		return self.fqs
