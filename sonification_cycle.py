from excel_parse import ExcelParser
from fq_converter import FqConverter
from pyo_module import PyoProcessing


class SonificationCycle:
	
	def __init__(self, filename, duration=10):
		self.filename = filename
		self.duration = duration
		
		self.parser = ExcelParser(filename)
		self.channels = self.parser.channels_num()
		self.points = self.parser.points_num()
		self.source = self.parser.parse()
		
		self.converter = FqConverter(self.source, self.channels, self.points)
		self.frequencies = self.converter.get_fqs()
		
		self.pyo = PyoProcessing(self.frequencies, self.channels, self.points, self.duration, self.filename)
		self.pyo.process()
