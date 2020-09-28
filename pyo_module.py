from pyo import *
import numpy as np
import os


class PyoProcessing:
	
	def __init__(self, array, num_channels, num_points, duration, name_sample):
		
		if duration < 10:
			self.duration = 10
		else:
			self.duration = duration
		self.name_sample = name_sample
		self.channels = num_channels
		self.points = num_points
		self.segment = duration / num_points
		
		self.raw_source = np.transpose(array)
		self.source = self.raw_source.flatten()
		for point in range(len(self.source)):
			if np.isnan(self.source[point]):
				self.source[point] = 0
			else:
				continue
		self.array1 = tuple(float(i) for i in self.source[0:(self.points + 1)])
		self.array2 = tuple(float(i) for i in self.source[(self.points + 1):(2 * self.points + 1)])
		self.array3 = tuple(float(i) for i in self.source[(2 * self.points + 1):-1])
		# self.array2 = self.source[(self.points + 1):(2 * self.points + 1)]
		# self.array3 = self.source[-self.points]
		
	def process(self):
		s = Server(audio='offline').boot()
		
		# Path of the recorded sound file.
		path = os.path.join("./wav_files", f"{self.name_sample}.wav")
		
		# Setting the record options
		s.recordOptions(dur=self.duration, filename=path, fileformat=0, sampletype=1)
		
		if self.channels == 1:
			self.synth1(self.array1, self.segment)
		elif self.channels == 2:
			self.synth1(self.array1, self.segment)
			self.synth2(self.array2, self.segment)
		elif self.channels == 3:
			self.synth1(self.array1, self.segment)
			self.synth2(self.array2, self.segment)
			self.synth3(self.array3, self.segment)
			
		s.recstart()
		s.start()
		s.shutdown()
	
	@staticmethod
	def synth1(array, segment):
		frequencies = iter(array)
		fqs = SigTo(value=array[0], init=200)
		synth = SineLoop(freq=fqs, mul=.2).out()
		
		def pick_new_freq():
			try:
				fqs.value = next(frequencies)
			except StopIteration:
				fqs.value = array[-1]
			
		pat = Pattern(function=pick_new_freq, time=segment).play()
	
	@staticmethod
	def synth2(array, segment):
		frequencies = iter(array)
		fqs = SigTo(value=array[0], init=200)
		tab = SawTable(order=5).normalize()
		synth = Osc(table=tab, freq=fqs, mul=.2).out()
		
		def pick_new_freq():
			try:
				fqs.value = next(frequencies)
			except StopIteration:
				fqs.value = array[-1]
		
		pat = Pattern(function=pick_new_freq, time=segment).play()
	
	@staticmethod
	def synth3(array, segment):
		frequencies = iter(array)
		fqs = SigTo(value=array[0], init=200)
		tab = SquareTable(order=5).normalize()
		synth = Osc(table=tab, freq=fqs, mul=.2).out()
		
		def pick_new_freq():
			try:
				fqs.value = next(frequencies)
			except StopIteration:
				fqs.value = array[-1]
		
		pat = Pattern(function=pick_new_freq, time=segment).play()
