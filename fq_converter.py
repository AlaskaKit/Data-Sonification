import numpy as np
from prepack import Prepack


class FqConverter:
	"""
	Converter class for user's source array.
	Maps the frequency for the every value in the user's array.
	
	Properties:
		self.largest: maximum in the users's array.
		self.smallest: minimum in the user's array.
		self.gap: range between them
		self.source: user's array from the prepack instance
		self.fqs: array with the frequencies mapped.
		
	"""
	def __init__(self, prepack=Prepack):
		"""
		A constructor. Reads the prepack instance, writes the propertis, finds min. max and gap.
		Checks if there is at least two valid points in the array.
		:param prepack: an instance of the Prepack class with properties rewritten with user's data characteristics.
		:raises: ValueError if there is less than two valid points in the array.
		"""
		
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
		"""
		Protected method for converting one given point to the frequency. Contains the converting algorithm.
		:param point: float number or none
		:return: frequency: float number
		"""
		if point is None:
			return 0
		else:
			ratio = (point - self.smallest) / self.gap
			fq = 220 * 2 ** (2 * ratio)
			return fq
		
	def get_fqs(self):
		"""
		Public method for converting. Vectorizes the __covert method and maps it to the user's array.
		:return: an array of frequencies in range from 220. to 880.
		"""
		vect_converter = np.vectorize(self.__convert)
		self.fqs = vect_converter(self.source)
		return self.fqs
