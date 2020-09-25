import numpy as np
import xlrd


class ExcelParser:
	def __init__(self, xlsfile):
		self.inputWorkbook = xlrd.open_workbook(xlsfile)
		self.inputWorksheet = self.inputWorkbook.sheet_by_index(0)
		self.values = np.full((self.inputWorksheet.nrows, self.inputWorksheet.ncols), None)
	
	# TODO: add checks
	
	def parse(self):
		for x in range(self.inputWorksheet.ncols):
			for y in range(self.inputWorksheet.nrows):
				if not self.inputWorksheet.cell_value(y, x):
					self.values[y][x] = None
				else:
					self.values[y][x] = self.inputWorksheet.cell_value(y, x)
				
	def __str__(self):
		return self.values
