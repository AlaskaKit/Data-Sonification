from abc import abstractmethod
import os
import numpy as np
import xlrd
import csv


# Interface
class AParser:
	@abstractmethod
	def parse(self):
		pass
	
	def channels_num(self):
		pass
	
	def points_num(self):
		pass


# Strategy 1
class ExcelParser(AParser):
	
	def __init__(self, xlsfile: str):
		try:
			self.inputWorkbook = xlrd.open_workbook(xlsfile)
		except Exception:
			raise Exception("Unable to locate the file or invalid file format.")
		
		self.inputWorksheet = self.inputWorkbook.sheet_by_index(0)
		
		if self.inputWorksheet.nrows == 0:
			raise ValueError("Unable to detect any data in the file.")
		
		self.values = np.full((self.inputWorksheet.nrows, 3), None)
	
	def parse(self):
		for x in range(self.inputWorksheet.ncols):
			if x >= 3:
				break
			else:
				for y in range(self.inputWorksheet.nrows):
					if y >= 300:
						break
					else:
						
						if not self.inputWorksheet.cell_value(y, x):
							self.values[y][x] = None
						elif isinstance(self.inputWorksheet.cell_value(y, x), (float, int)):
							self.values[y][x] = self.inputWorksheet.cell_value(y, x)
						else:
							raise ValueError("Invalid data format in the file.")
		return self.values
	
	def channels_num(self):
		return self.inputWorksheet.ncols
	
	def points_num(self):
		return self.inputWorksheet.nrows


# Strategy 2
class CSVParser(AParser):
	def __init__(self, csvfile: str):
		self.csvpath = csvfile
		self.inputfile = []
		self.output = None
		self.lines = 0
	
	def __get_delimiter(self):
		with open(self.csvpath, 'r', newline='') as file:
			sniffer = csv.Sniffer()
			dialect = sniffer.sniff(file.read())
			dlmtr = dialect.delimiter
			return dlmtr
		
	@staticmethod
	def __float_checker(float_string):
		"""It takes a float string ("1,23" or "1,234.567.890") and
		converts it to floating point number (1.23 or 1.234567890).
		"""
		float_string = str(float_string)
		
		try:
			if float_string.count(".") == 1 and float_string.count(",") == 0:
				return float(float_string)
			else:
				semi_string = list(float_string)
				while semi_string.count(".") != 0:
					semi_string.remove(".")
				out_string = str.replace("".join(semi_string), ",", ".")
			return float(out_string)
		except ValueError:
			raise ValueError("Invalid data format in the file.")
	
	def parse(self):
		try:
			dlmtr = self.__get_delimiter()
		except Exception:
			raise Exception("Unable to locate the file or invalid file format.")
		
		with open(self.csvpath, 'r', newline='') as file:
			reader = csv.reader(file, delimiter=dlmtr)
			
			for line in reader:
				self.inputfile.append(line[:3])
				self.lines += 1
				if self.lines >= 300:
					break
				
		if self.inputfile == [[]]:
			raise ValueError("Unable to detect any data in the file.")
			
		self.output = np.full((len(self.inputfile), 3), None)
		for y in range(len(self.inputfile)):
			for x in range(len(self.output[y])):
				if self.inputfile[y][x] == "":
					self.output[y][x] = None
				else:
					self.output[y][x] = self.__float_checker(self.inputfile[y][x])
					
		return self.output
	
	def channels_num(self):
		return len(self.inputfile[0])
	
	def points_num(self):
		return self.lines


# Context
class GeneralParser:
	def __init__(self, path: str):
		
		self.ext = os.path.splitext(path)[1]
		
		if self.ext.lower() == '.xls' or self.ext.lower() == '.xlsx':
			self.__parser = ExcelParser(path)
		elif self.ext.lower() == '.csv':
			self.__parser = CSVParser(path)
		else:
			raise TypeError('Unable to locate the file or invalid file format.')
	
	def parse(self):
		return self.__parser.parse()
	
	def channels_num(self):
		return self.__parser.channels_num()
	
	def points_num(self):
		return self.__parser.points_num()
