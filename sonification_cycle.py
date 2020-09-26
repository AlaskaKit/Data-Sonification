from excel_parse import ExcelParser
from fq_converter import FqConverter






if __name__ == '__main__':
	parsed_sample = ExcelParser('Sample4.xlsx')
	# print(parsed_sample.parse())
	converter = FqConverter(parsed_sample.parse(), parsed_sample.channels_num(), parsed_sample.points_num())
	print(converter.get_fqs())
	