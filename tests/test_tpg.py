import unittest
from cocotbext.vidio.tpg import generate_frame 

class Test_generate_frame(unittest.TestCase):
	
	def test_generate_frame(self):
		axi_frame = generate_frame(8, 8, 2, 10, "p_incr")
		tuser = axi_frame[0].tuser
		self.assertEqual(tuser, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

unittest.main()