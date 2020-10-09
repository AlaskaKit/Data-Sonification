import unittest
import numpy as np
from general_parser import *
from config import *
import os



class TestGeneralParser(unittest.TestCase):
	
	# creating control arrays
	def setUp(self):
		self.controlarray1 = np.array(
			[(1.1059, None, None), (0.9864, None, None), (1.2384, None, None), (1.7864, None, None),
			 (2.0348, None, None), (4.431, None, None), (1.0158, None, None)])
		self.array1_channels = 1
		self.array1_points = 7
		
		
		self.controlarray2 = np.array(
			[(1.1059, 4.0321, None), (0.9864, 5.4658, None), (1.2384, -2.0358, None), (1.7864, -4.5874, None),
			 (2.0348, 6.5841, None), (4.431, 2.6874, None), (1.0158, -3.5494, None)])
		self.array2_channels = 2
		self.array2_points = 7
		
		self.controlarray3 = np.array(
			[(1.1059, 4.0321, 5.2484), (0.9864, 5.4658, -1.5789), (1.2384, -2.0358, 4.8452), (1.7864, -4.5874, -2.2498),
			 (2.0348, 6.5841, 1.2546), (4.431, 2.6874, -3.5498), (1.0158, -3.5494, 2.5496)])
		self.array3_channels = 3
		self.array3_points = 7
		
	# test scenario 1.5
	def test_call(self):
		# sc 1.5a
		with self.assertRaises(TypeError):
			t1_5a = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.5a.jpg"))
			t1_5a.parse()
			
		# sc 1.5b
		with self.assertRaises(TypeError):
			t1_5b = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1_5b"))
			t1_5b.parse()
	
	# test scenarios 1.1, 1.2, 1,3, 1.4
	def test_parse(self):
		
		# sc 1.1a
		t1_1a = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.1a.xlsx"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_1a.parse()[:, 0], self.controlarray1[:, 0]))
		except TypeError:
			pass
		self.assertEqual(t1_1a.points_num(), self.array1_points)
		self.assertEqual(t1_1a.channels_num(), self.array1_channels)
		
		# sc 1.1b
		t1_1b = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.1b.xlsx"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_1b.parse()[:, 1], self.controlarray1[:, 1]))
		except TypeError:
			pass
		self.assertEqual(t1_1b.points_num(), self.array2_points)
		self.assertEqual(t1_1b.channels_num(), self.array2_channels)
		# sc 1.1c
		t1_1c = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.1c.xlsx"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_1c.parse()[:, 2], self.controlarray1[:, 2]))
		except TypeError:
			pass
		self.assertEqual(t1_1c.points_num(), self.array3_points)
		self.assertEqual(t1_1c.channels_num(), self.array3_channels)
		
		# sc 1.2a
		t1_2a = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.2a.csv"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_2a.parse()[:, 0], self.controlarray1[:, 0]))
		except TypeError:
			pass
		
		self.assertEqual(t1_2a.points_num(), self.array1_points)
		self.assertEqual(t1_2a.channels_num(), self.array1_channels)
		
		# sc 1.2b
		t1_2b = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.2b.csv"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_2b.parse()[:, 1], self.controlarray1[:, 1]))
		except TypeError:
			pass
		
		self.assertEqual(t1_2b.points_num(), self.array2_points)
		self.assertEqual(t1_2b.channels_num(), self.array2_channels)
		
		# sc 1.2c
		t1_2c = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.2c.csv"))
		try:
			self.assertIsNone(np.testing.assert_array_almost_equal(t1_2c.parse()[:, 2], self.controlarray1[:, 2]))
		except TypeError:
			pass
		
		self.assertEqual(t1_2c.points_num(), self.array3_points)
		self.assertEqual(t1_2c.channels_num(), self.array3_channels)
		
		# sc 1.3a
		with self.assertRaises(ValueError):
			t1_3a = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.3a.xlsx"))
			t1_3a.parse()
			
		# sc 1.3b
		with self.assertRaises(ValueError):
			t1_3b = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.3b.csv"))
			t1_3b.parse()
			
		# sc 1.4a
		with self.assertRaises(TypeError):
			t1_4a = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.4a.xlsx"))
			t1_4a.parse()
			
		# sc 1.4b
		with self.assertRaises(TypeError):
			t1_4b = GeneralParser(os.path.join(TestingConfig.SRC_UPLOADS, "scenario1.4b.csv"))
			t1_4b.parse()


if __name__ == "__main__":
	unittest.main()
