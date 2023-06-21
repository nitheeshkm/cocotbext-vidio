import unittest

from cocotbext.vidio import GenAXIStream
from cocotbext.vidio.utils import axis2mat

class Test_tpg(unittest.TestCase):
	def test_GenRGBAXIStream(self):
		axi_frame = GenAXIStream(8, 8, 2, 10, "p_incr")
		tuser = axi_frame[0].tuser
		self.assertEqual(tuser, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

class Test_utils(unittest.TestCase):
	pass


# unittest.main()
if __name__=="__main__":
	axis = GenAXIStream(16,4,4,10,0,2)
	print((axis[0]))