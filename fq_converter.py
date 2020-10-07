import numpy as np
from prepack import Prepack

class FqConverter:
	def __init__(self, prepack=Prepack):
		
		if not isinstance(prepack, Prepack):
			raise TypeError("Critical error: prepack instance invalid. Contact the developer.")
		
		self.largest = None
		self.smallest = None
		self.source = prepack.source
		self.fqs = np.full((prepack.points, prepack.channels), 0, dtype=float)
		
		for x in range(prepack.channels):
			for y in range(prepack.points):
				if self.largest is None:
					self.largest = prepack.source[y][x]
				elif prepack.source[y][x] is None:
					continue
				elif prepack.source[y][x] > self.largest:
					self.largest = prepack.source[y][x]
				else:
					continue
		
		for x in range(prepack.channels):
			for y in range(prepack.points):
				if self.smallest is None:
					self.smallest = prepack.source[y][x]
				elif prepack.source[y][x] is None:
					continue
				elif prepack.source[y][x] < self.smallest:
					self.smallest = prepack.source[y][x]
				else:
					continue
		
		if self.largest is None or self.smallest is None or self.largest == self.smallest:
			raise ValueError("Must be at least two valid points in the array.")
		
		self.gap = self.largest - self.smallest
		
	def __convert(self, point):
		if point is None:
			return 0
		else:
			ratio = (point - self.smallest) / self.gap
			fq = 220 * 2 ** (2 * ratio)
			return fq
		
	def get_fqs(self):
		vect_converter = np.vectorize(self.__convert)
		self.fqs = vect_converter(self.source)
		return self.fqs
