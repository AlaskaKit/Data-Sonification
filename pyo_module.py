from pyo import *
from config import *
from prepack import Prepack
import numpy as np
import os


class PyoProcessing:
	"""
	Class for the sonification itself based on the Pyo library.
	
	"""
	def __init__(self, prepack = Prepack):
		"""
		Constructor.
		Reads the properties of the prepack instance.
		Splits the user's array into three tuples for the separate sonification.
		:param prepack: a prepack instance with certain properties rewritten with user's data characteristics.
		"""
		if not isinstance(prepack, Prepack):
			raise TypeError("Critical error: prepack instance invalid. Contact the developer.")
		
		self.duration = prepack.duration
		self.name_sample = prepack.filename
		self.channels = prepack.channels
		self.points = prepack.points
		self.segment = prepack.duration / prepack.points
		
		self.raw_source = np.transpose(prepack.source)
		self.source = self.raw_source.flatten()
		
		self.array1 = tuple(float(i) for i in self.source[0:self.points])
		self.array2 = tuple(float(i) for i in self.source[self.points:(2 * self.points)])
		self.array3 = tuple(float(i) for i in self.source[(2 * self.points):])
		
		self.path = ""
		
	def process(self):
		"""
		A processor.
		Creates a pyo server, sets the record options.
		Creates certain number of oscillators (based on channels number from the Prepack).
			For each oscillators instances being created:
			- SigTo controlling object
			- Pattern object for changing the fq in the certain time intervals using pick_new_fq function.
			- pick_new_fq function, containing the iterator from the frequency tuple.
		Due to complex structure of each "channel" it is hard to collapse duplicate parts of the code into methods
		or functions, so here we have a massive "if" block.
		:return: a path to file recorded.
		"""
		s = Server(audio='offline').boot()
		
		# Path of the recorded sound file.
		self.path = os.path.join(ProductionConfig.WAV_FILES, f"{self.name_sample}.wav")
		
		# Setting the record options
		s.recordOptions(dur=self.duration, filename=self.path, fileformat=0, sampletype=1)
		
		if self.channels == 1:
			frequencies1 = iter(self.array1)
			fqs1 = SigTo(value=self.array1[0], init=200)
			synth1 = SineLoop(freq=fqs1, mul=.2).out()
			
			def pick_new_freq1():
				try:
					fqs1.value = next(frequencies1)
				except StopIteration:
					fqs1.value = self.array1[-1]
			
			pat1 = Pattern(function=pick_new_freq1, time=self.segment).play()
		
		elif self.channels == 2:
			frequencies1 = iter(self.array1)
			fqs1 = SigTo(value=self.array1[0], init=200)
			synth1 = SineLoop(freq=fqs1, mul=.2).out()
			
			def pick_new_freq1():
				try:
					fqs1.value = next(frequencies1)
				except StopIteration:
					fqs1.value = self.array1[-1]
			
			pat1 = Pattern(function=pick_new_freq1, time=self.segment).play()
			
			frequencies2 = iter(self.array2)
			fqs2 = SigTo(value=self.array2[0], init=200)
			tab2 = SawTable(order=5).normalize()
			synth2 = Osc(table=tab2, freq=fqs2, mul=.2).out()
			
			def pick_new_freq2():
				try:
					fqs2.value = next(frequencies2)
				except StopIteration:
					fqs2.value = self.array2[-1]
			
			pat2 = Pattern(function=pick_new_freq2, time=self.segment).play()
			
		elif self.channels == 3:
			frequencies1 = iter(self.array1)
			fqs1 = SigTo(value=self.array1[0], init=200)
			synth1 = SineLoop(freq=fqs1, mul=.2).out()
			
			def pick_new_freq1():
				try:
					fqs1.value = next(frequencies1)
				except StopIteration:
					fqs1.value = self.array1[-1]
			
			pat1 = Pattern(function=pick_new_freq1, time=self.segment).play()
			
			frequencies2 = iter(self.array2)
			fqs2 = SigTo(value=self.array2[0], init=200)
			tab2 = SawTable(order=5).normalize()
			synth2 = Osc(table=tab2, freq=fqs2, mul=.2).out()
			
			def pick_new_freq2():
				try:
					fqs2.value = next(frequencies2)
				except StopIteration:
					fqs2.value = self.array2[-1]
			
			pat2 = Pattern(function=pick_new_freq2, time=self.segment).play()
			
			frequencies3 = iter(self.array3)
			fqs3 = SigTo(value=self.array3[0], init=200)
			tab3 = SquareTable(order=5).normalize()
			synth3 = Osc(table=tab3, freq=fqs3, mul=.2).out()
			
			def pick_new_freq3():
				try:
					fqs3.value = next(frequencies3)
				except StopIteration:
					fqs3.value = self.array3[-1]
			
			pat3 = Pattern(function=pick_new_freq3, time=self.segment).play()
		
		s.recstart()
		s.start()
		s.shutdown()
		
		return self.path
