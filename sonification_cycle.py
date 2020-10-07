from general_parser import *
from prepack import Prepack
from fq_converter import FqConverter
from pyo_module import PyoProcessing


class SonificationCycle:
	
	def __init__(self, sourcepath, duration=10):
		
		if duration < 10:
			duration = 10
		else:
			duration = duration
		self.prepack = Prepack(sourcepath, duration)
		
		self.path_to_wav = ""
		
	def perform_cycle(self):
		# filetype-wise parsing via general parser
		try:
			parser = GeneralParser(self.prepack.sourcepath)
			self.prepack.set_source(parser.parse())
			self.prepack.set_channels(parser.channels_num())
			self.prepack.set_points(parser.points_num())
		except Exception:
			raise
		
		# converting numbers into frequencies
		try:
			converter = FqConverter(self.prepack)
			fqs = converter.get_fqs()
			self.prepack.set_source(fqs)
		except Exception:
			raise
		
		# pyo processing
		try:
			pyo = PyoProcessing(self.prepack)
			
			self.path_to_wav = pyo.process()
		except Exception:
			raise
