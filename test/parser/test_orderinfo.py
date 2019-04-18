'''
This test suite will check if the OrderInfo object is working as expected
'''
import unittest
from pydelivery.parser.parseround import OrderInfo

class Test_OrderInfo_Init(unittest.TestCase):
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo()
    self.assertEqual(e.exception.args[0], "__init__() missing 2 required positional arguments: 'name_or_number' and 'road'")
    
  def test_02_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo(None, None)
    self.assertEqual(e.exception.args[0], 'House must be identified by a string or integer')
    
  def test_03_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo('', None)
    self.assertEqual(e.exception.args[0], 'Must provide a non-empty house name')
    
  def test_04_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo('', '')
    self.assertEqual(e.exception.args[0], 'Must provide a non-empty house name')
    
  def test_05_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo(-1, None)
    self.assertEqual(e.exception.args[0], "House number should be a positive integer")
    
  def test_06_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo('Name', '')
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")
    
  def test_07_init(self):
    with self.assertRaises(TypeError) as e:
      oi = OrderInfo('Name', 0)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")
    
  def test_08_init(self):
    oi = OrderInfo('Name', 'Road')
