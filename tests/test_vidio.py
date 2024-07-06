import unittest

from cocotbext.vidio import GenAXIStream
from cocotbext.vidio.utils import axis2mat
from cocotbext.vidio import constants as const
from cocotbext.vidio import csc

class Test_tpg(unittest.TestCase):
	def test_GenRGBAXIStream(self):
		axi_frame = GenAXIStream(8, 8, 2, 10, "p_incr")
		tuser = axi_frame[0].tuser
		self.assertEqual(tuser, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

class Test_utils(unittest.TestCase):
	pass


# unittest.main()
if __name__=="__main__":
	axis, y420 = GenAXIStream(16, 4, 2, 10, const.Pattern.rand, const.ColorFormat.YUV420)
	print(y420)
	y422 = csc.y420to422(y420, 16, 4)
	print(y422)
