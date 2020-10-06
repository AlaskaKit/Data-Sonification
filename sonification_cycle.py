from excel_parse import ExcelParser
from fq_converter import FqConverter
from pyo_module import PyoProcessing


class SonificationCycle:
	
	def __init__(self, sourcepath, duration=10):
		self.sourcepath = sourcepath
		self.duration = duration
		
		#parsing
		self.parser = ExcelParser(self.sourcepath)
		self.channels = self.parser.channels_num()
		self.points = self.parser.points_num()
		self.fq_source = self.parser.parse()
		
		#converting
		self.converter = FqConverter(self.fq_source, self.channels, self.points)
		self.frequencies = self.converter.get_fqs()
		
			
		self.filename = self.sourcepath.split("\\")[-1]
		self.pyo = PyoProcessing(self.frequencies, self.channels, self.points, self.duration, self.filename)
		self.pyo.process()
