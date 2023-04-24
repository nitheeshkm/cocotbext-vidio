import unittest
from cocotbext.vidio import GenRGBAXIStream

class Test_tpg(unittest.TestCase):
	def test_GenRGBAXIStream(self):
		axi_frame = GenRGBAXIStream(8, 8, 2, 10, "p_incr")
		tuser = axi_frame[0].tuser
		self.assertEqual(tuser, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

class Test_utils(unittest.TestCase):
	pass


unittest.main()