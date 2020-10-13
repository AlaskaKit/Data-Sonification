from abc import abstractmethod
import os
import numpy as np
import xlrd
import csv


# Interface
class AParser:
	"""
	Interface class for the strategy pattern.
	Contains methods for the specific parsers.
	"""
	@abstractmethod
	def parse(self):
		pass
	
	@abstractmethod
	def channels_num(self):
		pass
	
	@abstractmethod
	def points_num(self):
		pass


# Strategy 1
class ExcelParser(AParser):
	
	"""
	Class for parsing Excel files. Based on xlrd library.
	
	Opens and reads excel file (if available), checks if there are any data.
	Limits the number of rows to equal or less than 300 and the number of columns equal or less than 3.
	
	:parameter: a path to the user's uploaded file (normally an attribute of the Prepack instance).
	
	attributes:
		self.inputWorkbook: xlrd instance which opens spreadsheet file for data extraction
		self.inputWorksheet: xlrd instance which contains the data for the first sheet in the workbook
		self.rows: total number of the rows in the user's file
		self.columns: total number of the columns in the user's file.
		self.values: an empty (filled with none) numpy array with limited size for storing user's value read.
		
	:raises:
		TypeError if the file couldn't be open
		ValueError if there are no data in the file.
	"""
	
	def __init__(self, xlsfile: str):
		try:
			self.inputWorkbook = xlrd.open_workbook(xlsfile)
		except Exception:
			raise TypeError("Unable to locate the file or invalid file format.")
		
		self.inputWorksheet = self.inputWorkbook.sheet_by_index(0)
		
		if self.inputWorksheet.nrows == 0:
			raise ValueError("Unable to detect any data in the file.")
		
		if self.inputWorksheet.nrows > 300:
			self.rows = 300
		else:
			self.rows = self.inputWorksheet.nrows
			
		self.values = np.full((self.rows, 3), None)
		
		if self.inputWorksheet.ncols > 2:
			self.cols = 3
		else:
			self.cols = self.inputWorksheet.ncols
		
		self.values = np.full((self.rows, 3), None)
	
	def parse(self):
		
		"""
		Parsing method.
		
		A cycle runs through the xlrd instance, checks the value and writes it to the self.values attribute.
		:raises ValueError if there is invalid data in the source array.
		:return: self.values array with user's data.
		"""
		
		for x in range(self.cols):
			for y in range(self.rows):
				if not self.inputWorksheet.cell_value(y, x):
					self.values[y][x] = None
				elif isinstance(self.inputWorksheet.cell_value(y, x), (float, int)):
					self.values[y][x] = self.inputWorksheet.cell_value(y, x)
				else:
					raise ValueError("Invalid data format in the file.")
		return self.values
	
	def channels_num(self):
		"""
		Method for getting the number of channels for writing to the particular attribute of the prepack instance.
		:return: number of the actual columns (channels) in the output array.
		"""
		return self.cols
	
	def points_num(self):
		"""
		Method for getting the number of points for writing to the particular attribute of the prepack instance.
		:return: number of the actual rows (points) in the output array.
		"""
		return self.rows


# Strategy 2
class CSVParser(AParser):
	
	"""
	Class for parsing csv files.
	
	Opens and reads csv file (if available), parses the delimiter in the file.
	Checks if there are any data, converts its format to the float (if possible), writes it to the output array.
	Limits the number of rows to equal or less than 300 and the number of columns equal or less than 3.
	
	:parameter: a path to the user's uploaded file (normally an attribute of the Prepack instance).
	
	attributes:
		self.csvpath: path to the csv file
		self.inputfile: an aemty list for storing the lines from the user's file
		self.lines: total number of the lines in the user's file
		self.ch: total number of the columns in the user's file.
		self.output: an empty variable for storing numpy array with user's values after the parsing.
	"""
	
	def __init__(self, csvfile: str):
		self.csvpath = csvfile
		self.inputfile = []
		self.output = None
		self.lines = 0
		
		self.ch = 0
	
	def __get_delimiter(self):
		"""
		Protected method for getting the delimiter from the user's file.
		"""
		with open(self.csvpath, 'r', newline='') as file:
			sniffer = csv.Sniffer()
			dialect = sniffer.sniff(file.read())
			dlmtr = dialect.delimiter
			return dlmtr
		
	@staticmethod
	def __float_checker(float_string):
		"""
		Protected method for converting a float string ("1,23" or "1,234.567.890")
		to floating point number (1.23 or 1.234567890).
		:parameter: float string
		:raises: ValueError in case of the incorrect user's data.
		:returns: float number
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
		"""
		Parsing method.
		Gets delimiter from the user's file (returns TypeError if unable to open the file).
		
		Reads the lines from the file, counts them and stores first three values of each line
		to the specific attribute with the limit of 300 lines.
		Checks if there is any lines stored.
		Checks the number of the actual columns (channels).
		Creates an output array, writes the user's data to it, converting to the float numbers simultaneously.
		:raises:
			TypeError if unable to open and read user's file.
			ValueError if there is no data in the source array.
		
		:return: self.output array with user's data.
		"""
		try:
			dlmtr = self.__get_delimiter()
			
		except Exception:
			raise TypeError("Unable to locate the file or invalid file format.")
		
		with open(self.csvpath, 'r', newline='') as file:
			reader = csv.reader(file, delimiter=dlmtr)
			
			for line in reader:
				self.inputfile.append(line[:3])
				self.lines += 1
				if self.lines >= 300:
					break
				
		if self.inputfile == [[]]:
			raise ValueError("Unable to detect any data in the file.")
		if dlmtr in {"\r", "\r\n", "\n"}:
			self.ch = 1
		else:
			self.ch = len(self.inputfile[0])
			
		self.output = np.full((len(self.inputfile), 3), None)
		for y in range(len(self.inputfile)):
			for x in range(len(self.inputfile[0])):
				if self.inputfile[y][x] == "":
					self.output[y][x] = None
				else:
					self.output[y][x] = self.__float_checker(self.inputfile[y][x])
					
		return self.output
	
	def channels_num(self):
		"""
		Method for getting the number of channels for writing to the particular attribute of the prepack instance.
		:return: number of the actual columns (channels) in the output array.
		"""
		return self.ch
	
	def points_num(self):
		"""
		Method for getting the number of points for writing to the particular attribute of the prepack instance.
		:return: number of the actual lines (points) in the output array.
		"""
		return self.lines


# Context
class GeneralParser:
	"""
	Context class for the strategy pattern.
	Reads the extension of the file (if any) and chooses the strategy (i.e. specific parser).
	Calls needed methods of the specific parsers.
	:parameter: path to the user's file.
	:raises: TypeError if there is no any file or file has invalid extension.
	:returns: the results of the parser's methods.
	"""
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
