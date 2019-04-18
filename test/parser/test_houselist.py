'''
This is the test suite for the HouseList object
'''

from pydelivery.parser.parseround import HouseList, HouseInfo
import unittest

# Declare some example HouseInfo instances
hi1 = HouseInfo('Name1', 'Road1', None)
hi2 = HouseInfo('Name1', 'Road2', None)
hi3 = HouseInfo('Name2', 'Road1', None)

class Test_HouseList(unittest.TestCase):
  def test_01_init(self):
    hl = HouseList()
    self.assertListEqual(hl, [])

  def test_02_init(self):
    hl = HouseList([hi1, hi2])
    self.assertListEqual(hl, [hi1, hi2])

  def test_03_equal(self):
    hl = HouseList([hi1, hi2])
    self.assertEqual(hl[0], hi1)
    
  def test_04_equal(self):
    hl = HouseList([hi1, hi2])
    self.assertEqual(hl[1], hi2)
    
  def test_05_equal(self):
    hl = HouseList([hi1, hi2])
    self.assertIsNone(hl[hi3])
    
  def test_06_equal(self):
    hl = HouseList([hi1, hi2])
    self.assertEqual(hl[hi1], hi1)
    
  def test_07_equal(self):
    hl = HouseList([hi1, hi2])
    with self.assertRaises(ValueError) as e:
      hl['Road1']
    self.assertEqual(e.exception.args[0], "Must pass either an integer or instance of 'HouseInfo'")
