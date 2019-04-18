'''
This is the test module for the TitleMap object
'''

from collections import OrderedDict
import unittest
from pydelivery.parser.parseround import TitleMap

class Mock_TitleMap(TitleMap):
  '''Class used by the test suite to avoid problems with a central mapping'''
  def __init__(self, *args, **kwds):
    super().__init__(*args, **kwds)
    self._map.clear()   # Ensure empty mapping prior to any test
    

class TestTitleMap(unittest.TestCase):
  def test_01_add_None(self):
    tm = Mock_TitleMap()
    tm.add('a', None)
    self.assertIsNone(tm['a'])
    
  def test_02_add_string(self):
    tm = Mock_TitleMap()
    tm.add('a', 'none')
    self.assertEqual(tm[0], 'a')
    
  def test_03_check_index(self):
    tm = Mock_TitleMap()
    tm.add('a', None)
    self.assertEqual(tm.index('a'), 0)
    
  def test_04_duplicate_error(self):
    tm = Mock_TitleMap()
    tm.add('a', None)
    with self.assertRaises(ValueError) as e:
      tm.add('a', 'none')
    self.assertEqual(e.exception.args[0], "Key 'a' already present")
    self.assertIsNone(tm['a'])
 
  def test_05_duplicate_type(self):
    tm = Mock_TitleMap()
    tm.add('a', None)
    with self.assertRaises(ValueError) as e:
      tm.add('a', 'none', update=True)
    self.assertEqual(e.exception.args[0], "Updating with different type: 'str' instead of 'NoneType'")
    
  def test_06_duplicate_silent(self):
    tm = Mock_TitleMap()
    tm.add('a', 5)
    tm.add('a', 10, update=True)
    self.assertEqual(tm['a'], 10)
        
  def test_07_remove_error(self):
    tm = Mock_TitleMap()
    with self.assertRaises(KeyError) as e:
      tm.remove('a', error=True)
    self.assertEqual(e.exception.args[0], "Key 'a' not present in mapping")
    
  def test_08_remove_silent(self):
    tm = Mock_TitleMap()
    tm.remove('a')
    
  def test_09_add_and_delete(self):
    tm = Mock_TitleMap()
    tm.add('a', '345')
    tm.add('b', '671')
    tm.remove('a')
    tm.add('a', '127')
    self.assertEqual(tm.index('a'), 1)
    self.assertEqual(tm['a'], '127')
    self.assertEqual(tm.index('b'), 0)
    self.assertEqual(tm['b'], '671')
 
  def test_10_index(self):
    'Test accessing by title'
    tm = Mock_TitleMap()
    tm.add('Telegraph')
    tm.add('Sun')
    tm.add('Express')
    self.assertEqual(tm.index('Express'), 2)
    self.assertEqual(tm[2], 'Express')
  
  def test_50_3way_error(self):
    'Test having multiple title mapping in use'
    tm1 = Mock_TitleMap()
    tm2 = Mock_TitleMap()
    tm3 = Mock_TitleMap()
    tm2.add('title1', 1)
    tm1.add('title2', 2)
    tm3.add('title3', 3)
    tm1.add('title4', 4)
    with self.assertRaises(ValueError) as e:
      tm3.add('title2', 5)
    self.assertEqual(e.exception.args[0], "Key 'title2' already present")
    self.assertEqual(tm1['title1'], 1)
    self.assertEqual(tm1['title2'], 2)
    self.assertEqual(tm1['title3'], 3)
    self.assertEqual(tm1['title4'], 4)
    
  def test_51_3way_silent(self):
    'Test having multiple title mapping in use'
    tm1 = Mock_TitleMap()
    tm2 = Mock_TitleMap()
    tm3 = Mock_TitleMap()
    tm2.add('title1', 1)
    tm1.add('title2', 2)
    tm3.add('title3', 3)
    tm1.add('title4', 4)
    tm3.add('title2', 5, update=True)
    self.assertEqual(tm1['title1'], 1)
    self.assertEqual(tm1['title2'], 5)
    self.assertEqual(tm1['title3'], 3)
    self.assertEqual(tm1['title4'], 4)
    
  def test_52_3way_modify(self):
    'Test having multiple title mapping in use'
    tm1 = Mock_TitleMap()
    tm2 = Mock_TitleMap()
    tm3 = Mock_TitleMap()
    tm2.add('title1', 1)
    tm1.add('title2', 2)
    tm3.add('title3', 3)
    tm1.add('title4', 4)
    tm3.add('title2', 5, update=True)
    tm2.remove('title4')
    self.assertEqual(tm1['title1'], 1)
    self.assertEqual(tm1['title2'], 5)
    self.assertEqual(tm1['title3'], 3)
    with self.assertRaises(KeyError):
      self.assertEqual(tm1['title4'], 4)


class TitleMap_MagOrder_Mixin(unittest.TestCase):
  pass


class Test_TitleMap_BeforePaper(unittest.TestCase):
  def test_01_init(self):
    tm = Mock_TitleMap(mag_order='before_paper')
    self.assertEqual(tm._magorder, 'before_paper')
    self.assertIsNotNone(tm._order)


class Test_TitleMap_AfterPaper(unittest.TestCase):
  def test_01_init(self):
    tm = Mock_TitleMap(mag_order='after_paper')
    self.assertEqual(tm._magorder, 'after_paper')
    self.assertIsNotNone(tm._order)


class Test_TitleMap_InwithPaper(unittest.TestCase):
  def test_01_init(self):
    tm = Mock_TitleMap(mag_order='inwith_paper')
    self.assertEqual(tm._magorder, 'inwith_paper')
    self.assertIsNone(tm._order)
    
class Test_TitleMap_Bad(unittest.TestCase):
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      Mock_TitleMap(mag_order='anywhere')
    self.assertEqual(e.exception.args[0], "Invalid magazine order given")
