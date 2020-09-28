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
		self.array1 = tuple(float(i) for i in self.source[0:(self.points)])
		self.array2 = tuple(float(i) for i in self.source[(self.points):(2 * self.points)])
		self.array3 = tuple(float(i) for i in self.source[(2 * self.points):])
		
		
	def process(self):
		s = Server(audio='offline').boot()
		
		# Path of the recorded sound file.
		path = os.path.join("./wav_files", f"{self.name_sample}.wav")
		
		# Setting the record options
		s.recordOptions(dur=self.duration, filename=path, fileformat=0, sampletype=1)
		
		if self.channels == 1:
			self.synth1()
		elif self.channels == 2:
			self.synth1()
			self.synth2()
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
			tab = SawTable(order=5).normalize()
			synth2 = Osc(table=tab, freq=fqs2, mul=.2).out()
			
			def pick_new_freq2():
				try:
					fqs2.value = next(frequencies2)
				except StopIteration:
					fqs2.value = self.array2[-1]
			
			pat = Pattern(function=pick_new_freq2, time=self.segment).play()
		
		s.recstart()
		s.start()
		s.shutdown()
		
		
	def synth3(self):
		frequencies = iter(self.array3)
		fqs = SigTo(value=self.array3[0], init=200)
		tab = SquareTable(order=5).normalize()
		synth = Osc(table=tab, freq=fqs, mul=.2).out()
		
		def pick_new_freq():
			try:
				fqs.value = next(frequencies)
			except StopIteration:
				fqs.value = self.array3[-1]
		
		pat = Pattern(function=pick_new_freq, time=self.segment).play()
