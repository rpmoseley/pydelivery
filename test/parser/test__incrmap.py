'''
This test will check that the _IncrMap object operates correctly
'''

import unittest
from pydelivery.parser.parseround import _IncrMap

class Test_IncrMap(unittest.TestCase):
  def test_01_incr(self):
    im = _IncrMap()
    im.increment('a')
    self.assertEqual(im._map['a'], 1)
    
  def test_02_incr(self):
    im = _IncrMap()
    im._map['a'] = '0'
    with self.assertRaises(ValueError) as e:
      im.increment('a')
    self.assertEqual(e.exception.args[0], "Key 'a' value must be an integer")
    
  def test_03_decr_notin(self):
    im = _IncrMap()
    im.decrement('a')
    self.assertNotIn('a', im)
    
  def test_04_decr_negative(self):
    im = _IncrMap()
    im['a'] = 0
    im._decr('a', autoremove=False)
    self.assertEqual(im['a'], 0)
    
  def test_05_decr_str(self):
    im = _IncrMap()
    im._map['a'] = '1'
    with self.assertRaises(ValueError) as e:
      im.decrement('a')
    self.assertEqual(e.exception.args[0], "Key 'a' value must be an integer")
    
  def test_06_incr_decr(self):
    im = _IncrMap()
    im._incr('a')
    im._decr('a', autoremove=False)
    self.assertEqual(im['a'], 0)
  
  def test_07_decr_autoremove(self):
    im = _IncrMap()
    im._incr('a')
    self.assertEqual(im['a'], 1)
    im._decr('a', autoremove=True)
    self.assertNotIn('a', im)

  def test_08_decr_error(self):
    im = _IncrMap()
    im._map['a'] = -1
    self.assertEqual(im['a'], -1)
    im._decr('a', autoremove=False)
    with self.assertRaises(ValueError) as e:
      im.decrement('a', error=True)
    self.assertEqual(e.exception.args[0], "Key 'a' cannot be negative")
    
  def test_09_add(self):
    im = _IncrMap()
    im._incr('a')
    im._incr('a')
    self.assertEqual(im['a'], 2)
    
  def test_10_remove(self):
    im = _IncrMap()
    im._incr('a')
    im._incr('a')
    im._decr('a')
    self.assertEqual(im['a'], 1)
    
  def test_11_iter(self):
    im = _IncrMap()
    im['a'] = 3
    im['c'] = 5
    im['c'] = 6
    im['b'] = 34
    im._incr('d')
    im._incr('d')
    im._incr('d')
    im._decr('c')
    imit = iter(im)
    self.assertEqual(next(imit), ('a', 1))
    self.assertEqual(next(imit), ('c', 1))
    self.assertEqual(next(imit), ('b', 1))
    self.assertEqual(next(imit), ('d', 3))
    with self.assertRaises(StopIteration):
      next(imit)
    
  def test_12_iter(self):
    im = _IncrMap()
    im['a'] = 1
    im['c'] = 1
    im['b'] = 1
    im._incr('d')
    imit = im.numeric_iter()
    self.assertEqual(next(imit), (0, 'a'))
    self.assertEqual(next(imit), (1, 'c'))
    self.assertEqual(next(imit), (2, 'b'))
    self.assertEqual(next(imit), (3, 'd'))
    with self.assertRaises(StopIteration):
      next(imit)
