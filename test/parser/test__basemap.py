'''
This module will test the base class of all the mapping objects, to check that the
shared functionality is working correctly without the overhead of the individual
mappings.
'''

from pydelivery.parser.parseround import _BaseMap
import unittest

class Mock__BaseMap(_BaseMap):
  def __init__(self, *args, **kwds):
    self._map = dict()
    super().__init__(*args, **kwds)

    
class Test__BaseMap(unittest.TestCase):
  def test_01_init(self):
    bm = _BaseMap()
    self.assertEqual(hasattr(bm, '_map'), True)
    
  def test_02_mapping(self):
    bm = _BaseMap()
    bm._add('item1', 1)
    self.assertEqual(bm['item1'], 1)
    
  def test_03_mock(self):
    bm = Mock__BaseMap()
    bm['a'] = 1
    self.assertEqual(bm['a'], 1)
    with self.assertRaises(ValueError) as e:
      bm._add('a', 2, ignoredup=False)
    self.assertEqual(e.exception.args[0], "Key 'a' already present")
    self.assertEqual(bm['a'], 1)

  def test_04_mock_ignoredup(self):
    bm = Mock__BaseMap()
    bm['a'] = 1
    self.assertEqual(bm['a'], 1)
    bm._add('a', 2)
    self.assertEqual(bm['a'], 1)
    
  def test_05_update_type(self):
    bm = _BaseMap()
    bm._add('a', 1)
    with self.assertRaises(ValueError) as e:
      bm._add('a', '1', update=True, ignoredup=False)
    self.assertEqual(e.exception.args[0], "Updating with different type: 'str' instead of 'int'")
    self.assertEqual(bm['a'], 1)
    
  def test_06_update_type(self):
    bm = _BaseMap()
    bm._add('a', 1)
    bm._add('a', '1', update=True)
    self.assertEqual(bm['a'], 1)
    
  def test_07_get_bad(self):
    bm = _BaseMap()
    bm._add('a', 1)
    bm._add('b', 2)
    self.assertEqual(bm[0], 'a')
    with self.assertRaises(KeyError) as e:
      self.assertEqual(bm[2], None)
    self.assertEqual(e.exception.args[0], "Element '2' does not exist")
    
  def test_08_index(self):
    bm = _BaseMap()
    bm['a'] = 1
    bm['b'] = 2
    self.assertEqual(bm._index('b'), 1)
    
  def test_09_bad_index(self):
    bm = _BaseMap()
    bm['a'] = 1
    bm['c'] = 3
    with self.assertRaises(KeyError) as e:
      bm._index('b')
    self.assertEqual(e.exception.args[0], "Key 'b' not present in mapping")
    
  def test_10_unhandled(self):
    bm = Mock__BaseMap()
    bm['a'] = 3
    bm['d'] = 5
    with self.assertRaises(ValueError) as e:
      bm[{'a'}]
    self.assertEqual(e.exception.args[0], "Unhandled item type for retrieval")
