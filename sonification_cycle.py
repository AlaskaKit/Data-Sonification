from general_parser import *
from prepack import Prepack
from fq_converter import FqConverter
from pyo_module import PyoProcessing


class SonificationCycle:
	"""
	A general class for performing the sonification process.
	"""
	def __init__(self, sourcepath, duration=10):
		"""
		A constructor. Creats an instance of the Prepack class.
		Checks and writes into the prepack duration value.
		:param sourcepath: str: path to the user's file/
		:param duration: float or int: value of the output sample duration in seconds.
		"""
		
		if duration < 10:
			duration = 10
		elif duration > 999:
			duration = 999
		else:
			duration = duration
		self.prepack = Prepack(sourcepath, duration)
		
		self.path_to_wav = ""
		
	def perform_cycle(self):
		"""
		One-by-one calling the sonification components in the proper order, passing them a prepack instance
		or just some of its properties.
		:raises: an unspecified range of the errors in case of getting them from the components.
		Raises them to the view object for flashing.
		:return: a path to the sample recorded.
		"""
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
