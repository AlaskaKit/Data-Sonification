import unittest
import numpy as np
from sonification_cycle import *
from config import *
import os


class TestSonificationCycle(unittest.TestCase):
	
	# creating control arrays
	def setUp(self):
		self.duration_small = 6
		
		self.duration_large = 6000
		
		self.sc3array = np.array(
			[(445.91164505, 641.13432495, 0.), (439.34800753, 765.97517875, 0.), (0., 301.9498146, 0.), (485.20208228, 220., 0.),
			 (500.39107085, 880., 0.), (673.66928127, 0., 0.), (440.9538111, 0., 0.)])
		
	# test scenario 2.3
	def test_call(self):
		# sc 2.3a
		t2_3a = SonificationCycle("", duration=self.duration_small)
		
		self.assertEqual(t2_3a.prepack.duration, 10)
		
		# sc 2.3b
		t2_3b = SonificationCycle("", duration=self.duration_large)
		
		self.assertEqual(t2_3b.prepack.duration, 999)
		
	# test scenarios 2.1, 2.2, 3
	def test_perform_cycle(self):
		
		# sc 1
		t2_1 = SonificationCycle(os.path.join(TestingConfig.SRC_UPLOADS, "scenario2.1.xlsx"), duration=30)
		t2_1.perform_cycle()
		t2_1source = t2_1.prepack.source.shape
		self.assertEqual(t2_1source, (300, 3))
		
		# sc 2.2
		with self.assertRaises(ValueError):
			t2_2 = SonificationCycle(os.path.join(TestingConfig.SRC_UPLOADS, "scenario2.2.xlsx"), duration=30)
			t2_2.perform_cycle()
			
		# sc 3
		t3 = SonificationCycle(os.path.join(TestingConfig.SRC_UPLOADS, "scenario3.xlsx"), duration=30)
		t3.perform_cycle()
		t3source = t3.prepack.source
		self.assertIsNone(np.testing.assert_array_almost_equal(t3source, self.sc3array))
		

if __name__ == "__main__":
	unittest.main()
