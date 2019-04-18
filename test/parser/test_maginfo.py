'''
This test suite will test the operation of the MagazineInfo object
'''
from pydelivery.parser.parseround import MagazineInfo
import unittest

class Test_MagInfo(unittest.TestCase):
  def test_01_init(self):
    mi = MagazineInfo('Magazine1', '4')
    self.assertEqual(mi.days, {4})
    self.assertEqual(mi._frequency, "W")
                     
  def test_02_init(self):
    mi = MagazineInfo('Magazine1', '4', frequency="2W")
    self.assertEqual(mi.days, {4})
    self.assertEqual(mi._frequency, "2W")
