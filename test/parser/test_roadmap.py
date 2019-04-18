'''
This module will test the RoadMap class within the parseround program.
'''

import unittest
from pydelivery.parser.parseround import RoadMap, HouseInfo

class Mock_HouseInfo(HouseInfo):
  def __init__(self, name_or_number, road):
    self._house = name_or_number
    self._road = road


class Mock_RoadMap(RoadMap):
  def __init__(self, *args, **kwds):
    super().__init__(*args, **kwds)
    self._map.clear()

    
class TestRoadMap_Init(unittest.TestCase):
  def test_01_create(self):
    rm = Mock_RoadMap()
    rm._incr('road1')
    self.assertEqual(rm['road1'], 1)
    
  def test_02_incr(self):
    rm = Mock_RoadMap()
    rm._incr('road1')
    self.assertEqual(rm['road1'], 1)
    rm._incr('road1')
    self.assertEqual(rm['road1'], 2)
    
  def test_03_decr_ok(self):
    rm = Mock_RoadMap()
    rm._incr('road1')
    self.assertEqual(rm['road1'], 1)
    rm._incr('road1')
    self.assertEqual(rm['road1'], 2)
    rm._decr('road1')
    self.assertEqual(rm['road1'], 1)
    
  def test_04_decr_err_off(self):
    rm = Mock_RoadMap()
    rm._decr('road1')
    self.assertNotIn('road1', rm)
    
  def test_05_decr_err_on(self):
    rm = Mock_RoadMap()
    with self.assertRaises(ValueError) as e:
      rm._decr('road1', error=True)
    self.assertEqual(e.exception.args[0], "Key 'road1' not present in mapping")

class TestRoadMap_Oper(unittest.TestCase):
  def test_01_remove(self):
    rm = Mock_RoadMap()
    hi = Mock_HouseInfo('House', 'road1')
    rm.add(hi)
    self.assertEqual(rm['road1'], 1)
    rm.remove(hi)
    self.assertNotIn('road1', rm)

  def test_02_remove(self):
    rm = Mock_RoadMap()
    with self.assertRaises(ValueError) as e:
      rm.remove(Mock_HouseInfo('House', 'Road1'), error=True)
    self.assertEqual(e.exception.args[0], "Key 'Road1' not present in mapping")

  def test_03_remove(self):
    rm = Mock_RoadMap()
    with self.assertRaises(ValueError) as e:
      rm.remove('Road1')
    self.assertEqual(e.exception.args[0], "Must pass an instance of HouseInfo")
    
  def test_04_remove(self):
    rm = Mock_RoadMap()
    rm.remove(Mock_HouseInfo('House', 'Road1'))
    self.assertIsNot('Road1', rm)
    
  def test_05_add(self):
    rm = Mock_RoadMap()
    with self.assertRaises(ValueError) as e:
      rm.add('Road1')
    self.assertEqual(e.exception.args[0], "Must pass an instance of HouseInfo")
    self.assertNotIn('Road1', rm)
    
  def test_06_add(self):
    rm = Mock_RoadMap()
    rm.add(Mock_HouseInfo('House', 'Road1'))
    self.assertIn('Road1', rm)
