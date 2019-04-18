'''
This is a test suite that will check if the _LimitList mixin class is correctly
operating on a specific object instance
'''

import unittest
from pydelivery.parser.parseround import _LimitList, HouseInfo, PaperInfo

pi = PaperInfo('Paper')
hi1 = HouseInfo(1, 'Road1', pi)
hi2 = HouseInfo('Name1', 'Road1', pi)
hi3 = HouseInfo('Name2', 'Road2', pi)

class Check_HouseList(_LimitList):
  def __init__(self, elems=None):
    super().__init__(HouseInfo, 'HouseInfo', elems)
    

class Test__LimitList(unittest.TestCase):
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      ll = _LimitList()
    self.assertEqual(e.exception.args[0], "__init__() missing 2 required positional arguments: 'type_' and 'name'")
    
  def test_02_init(self):
    with self.assertRaises(TypeError) as e:
      ll = _LimitList(HouseInfo)
    self.assertEqual(e.exception.args[0], "__init__() missing 1 required positional argument: 'name'")
  
  def test_03_init(self):
    class Mock_Type:
      pass
    ll = _LimitList(Mock_Type, 'Mock_Type')
    with self.assertRaises(ValueError) as e:
      ll.append(hi1)
    self.assertEqual(e.exception.args[0], "All elements must be 'Mock_Type' instances")
    
  def test_04_init(self):
    ll = Check_HouseList()
    self.assertEqual(issubclass(ll._type, HouseInfo), True)
    self.assertEqual(ll._name, 'HouseInfo')
  
  def test_05_init(self):
    ll = Check_HouseList(None)
    self.assertEqual(len(ll), 0)
    
  def test_06_init(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList([])
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'HouseInfo' instance")
    
  def test_07_flatten(self):
    ll = Check_HouseList()
    res = ll._flatten(hi1)
    self.assertEqual(res, [hi1])

  def test_08_flatten(self):
    ll = Check_HouseList(hi1)
    self.assertEqual(ll, [hi1])
    
  def test_09_flatten(self):
    ll = Check_HouseList()
    res = ll._flatten([hi1, [hi2, (hi3,)]])
    self.assertEqual(res, [hi1, hi2, hi3])
    
  def test_10_flatten(self):
    ll = Check_HouseList([hi1, [hi2, (hi3,)]])
    self.assertEqual(ll, [hi1, hi2, hi3])
  
  def test_11_flatten(self):
    ll = _LimitList(str, 'String', ['a', 'b', 'c'])
    with self.assertRaises(ValueError) as e:
      ll._all([1, 2, 3], _flatten=False)
    self.assertEqual(e.exception.args[0], "Must provide a sequence of 'String' instances")
    
  def test_12_flatten(self):
    ll = _LimitList(str, 'String', ['a', 'b', 'c'])
    self.assertIsNone(ll._all([1, 2, 3], except_=None, _flatten=False))
    
  def test_13_all(self):
    ll = Check_HouseList()
    with self.assertRaises(ValueError) as e:
      ll._all([hi1, pi, hi2])
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
    
  def test_14_equal(self):
    ll1 = Check_HouseList(hi1)
    self.assertListEqual(ll1, [hi1])
    
  def test_15_equal(self):
    ll1 = Check_HouseList(hi1)
    ll2 = Check_HouseList(hi1)
    self.assertListEqual(ll1, ll2)
    
  def test_16_equal(self):
    ll1 = Check_HouseList(hi1)
    ll2 = Check_HouseList([hi1,hi2])
    self.assertFalse(ll1 == ll2)
  
  def test_17_equal(self):
    ll1 = Check_HouseList(hi1)
    ll2 = _LimitList(PaperInfo, 'PaperInfo', pi)
    self.assertFalse(ll1 == ll2)
  
  def test_18_equal(self):
    ll1 = Check_HouseList(hi1)
    ll2 = Check_HouseList(hi2)
    self.assertFalse(ll1 == ll2)
    
  def test_20_append(self):
    with self.assertRaises(TypeError) as e:
      ll = Check_HouseList()
      ll.append()
    self.assertEqual(e.exception.args[0], "append() missing 1 required positional argument: 'elem'")
    
  def test_21_append(self):
    ll = Check_HouseList()
    ll.append(hi1)
    self.assertListEqual(ll, [hi1])
    
  def test_22_append(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.append([hi1, hi2])
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
    
  def test_23_append(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.extend(dict(a=1, b=2))
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
    
  def test_24_append(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.extend(pi)
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
    
  def test_25_extend(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.extend()
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'HouseInfo' instance")
    
  def test_26_extend(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.extend([])
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'HouseInfo' instance")
    
  def test_27_extend(self):
    ll = Check_HouseList()
    ll.extend(hi1)
    self.assertListEqual(ll, [hi1])
    
  def test_28_extend(self):
    ll = Check_HouseList()
    ll.extend([hi1, hi2])
    self.assertEqual(ll, [hi1, hi2])
    
  def test_29_extend(self):
    with self.assertRaises(ValueError) as e:
      ll = Check_HouseList()
      ll.extend(dict(a=1, b=2))
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
    
  def test_30_iadd(self):
    ll = Check_HouseList()
    ll += hi1
    self.assertListEqual(ll, [hi1])
    
  def test_31_iadd(self):
    ll = Check_HouseList()
    ll += [hi1]
    self.assertListEqual(ll, [hi1])
    
  def test_32_iadd(self):
    ll = Check_HouseList()
    ll += [hi1, hi2]
    self.assertListEqual(ll, [hi1, hi2])
    
  def test_33_remove(self):
    ll = Check_HouseList([hi1, hi2])
    with self.assertRaises(ValueError) as e:
      ll.remove(hi3)
    self.assertEqual(e.exception.args[0], "list.remove(x): x not in list")
    
  def test_34_remove(self):
    ll = Check_HouseList([hi1, hi2, hi3])
    ll.remove(hi2)
    self.assertListEqual(ll, [hi1, hi3])
    
  def test_36_insert(self):
    ll = Check_HouseList([hi1, hi3])
    ll.insert(1, hi2)
    self.assertListEqual(ll, [hi1, hi2, hi3])
    
  def test_37_insert(self):
    ll = Check_HouseList([hi1, hi3])
    with self.assertRaises(ValueError) as e:
      ll.insert(1, None)
    self.assertEqual(e.exception.args[0], "Must pass a single instance of 'HouseInfo'")
    
  def test_38_insert(self):
    ll = Check_HouseList([hi1, hi3])
    with self.assertRaises(ValueError) as e:
      ll.insert(1, [hi2])
    self.assertEqual(e.exception.args[0], "Must pass a single instance of 'HouseInfo'")
    
  def test_39_clear(self):
    ll = Check_HouseList([hi1, hi2, hi3])
    ll.clear()
    self.assertListEqual(ll, [])
    
  def test_40_recursive(self):
    ll = Check_HouseList([hi1, [hi2, hi3]])
    ll.remove([[hi2, hi3]])
    
  def test_41_contains(self):
    ll = Check_HouseList([hi1])
    self.assertTrue(hi1 in ll)
    
  def test_42_contains(self):
    ll = Check_HouseList([hi1, hi2])
    self.assertTrue([hi1, hi2] in ll)
    
    
