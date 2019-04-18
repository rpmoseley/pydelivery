'''
This is the test suite for the RoundInfo object which incorporates the other related objects
into a single entity.
'''

import unittest
from pydelivery.parser.parseround import RoundInfo, HouseInfo, PaperInfo, OrderInfo, OrderList

class TestRoundInfo_Init(unittest.TestCase):
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo()
    self.assertEqual(e.exception.args[0], "__init__() missing 2 required positional arguments: 'number' and 'name'")
    
  def test_02_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo(None)
    self.assertEqual(e.exception.args[0], "__init__() missing 1 required positional argument: 'name'")

  def test_03_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo(None, None)
    self.assertEqual(e.exception.args[0], "Must provide a number for the round")
    
  def test_04_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo(-1, '')
    self.assertEqual(e.exception.args[0], "Must provide a positive number for round")
    
  def test_05_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo(1, '')
    self.assertEqual(e.exception.args[0], "Must provide a name for the round")

  def test_06_init(self):
    ri = RoundInfo(1, 'Round1')
    self.assertEqual(ri._number, 1)
    self.assertEqual(ri._name, 'Round1')
    self.assertEqual(ri._houses, [])
    self.assertIsNone(ri._order)
  
  def test_07_init(self):
    hi1 = Mock_HouseInfo('Name1', 'Road1')
    hi2 = ('Name2', 'Road1')
    with self.assertRaises(ValueError) as e:
      RoundInfo(1, 'Round1', [hi1, hi2])
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
  
  def test_08_init(self):
    with self.assertRaises(ValueError) as e:
      RoundInfo(1, 'Round1', [])
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'HouseInfo' instance")
  
  def test_09_init(self):
    with self.assertRaises(ValueError) as e:
      RoundInfo(1, 'Round1', 'Name1')
    self.assertEqual(e.exception.args[0], "All elements must be 'HouseInfo' instances")
  
  def test_10_init(self):
    with self.assertRaises(ValueError) as e:
      ri = RoundInfo(1, 'Round1', None, [])
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'OrderInfo' instance")
  
  def test_11_init(self):
    oi = [HouseInfo('Name', 'Road1', PaperInfo('Telegraph')), OrderInfo('Name', 'Road')]
    with self.assertRaises(ValueError) as e:
      ri = RoundInfo(1, 'Round1', None, oi)
    self.assertEqual(e.exception.args[0], "All elements must be 'OrderInfo' instances")
  
  def test_12_init(self):
    with self.assertRaises(TypeError) as e:
      ri = RoundInfo(6, 'Round1', None, OrderList())
    self.assertEqual(e.exception.args[0], "Attempt to use round above maximum allowed")

  def test_13_init(self):
    ri = RoundInfo(1, 'Round1', None, OrderList())
    self.assertIsInstance(ri._order, OrderList)


# Provide a mock version of the HouseInfo object to perform tests against
class Mock_HouseInfo(HouseInfo):
  def __init__(self, name_or_number, road, paper=None, use_box=None):
    self._house = name_or_number
    self._road = road
    self._paper = paper or []

mhi1 = Mock_HouseInfo(14, 'Road1')
mhi2 = Mock_HouseInfo('House1', 'Road2')

class TestRoundInfo_Oper(unittest.TestCase):
  def test_01_house_type(self):
    ri = RoundInfo(1, 'Round1')
    oi = OrderInfo(14, 'Road1')
    with self.assertRaises(ValueError) as e:
      ri.add_house(oi)
    self.assertEqual(e.exception.args[0], "Can only add instances of HouseInfo")
    
  def test_02_house_type(self):
    ri = RoundInfo(1, 'Round1')
    ri.add_house(mhi1)
    self.assertEqual(ri._houses, [mhi1])
    
  def test_03_house_duplicate(self):
    ri = RoundInfo(1, 'Round1')
    ri._houses.append(mhi1)      # Prepopulate list of houses
    with self.assertRaises(ValueError) as e:
      ri.add_house(mhi1)
    self.assertEqual(e.exception.args[0], "House is already present in round")
    
  def test_04_house_remove(self):
    ri = RoundInfo(1, 'Round1', [mhi1])
    oi = OrderInfo(14, 'Road1')
    with self.assertRaises(ValueError) as e:
      ri.rem_house(oi)
    self.assertEqual(e.exception.args[0], "Can only remove instances of HouseInfo")
    
  def test_06_house_remove(self):
    ri = RoundInfo(1, 'Round1', [mhi1])
    with self.assertRaises(ValueError) as e:
      ri.rem_house(mhi2)
    self.assertEqual(e.exception.args[0], "House not present in round")
    
  def test_07_house_remove(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    ri.rem_house(mhi2)
    self.assertEqual(ri._houses, [mhi1])
    
  def test_08_house_remove(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    ri.rem_house(mhi1)
    self.assertEqual(ri._houses, [mhi2])
    
  def test_09_house_remove(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    ri.rem_house(mhi1)
    ri.rem_house(mhi2)
    self.assertEqual(ri._houses, [])
    with self.assertRaises(ValueError) as e:
      ri.rem_house(mhi1)
    self.assertEqual(e.exception.args[0], "House not present in round")
    
  def test_10_house_iter(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    riit = ri.house_iter()
    self.assertEqual(next(riit), mhi1)
    self.assertEqual(next(riit), mhi2)
    with self.assertRaises(StopIteration):
      next(riit)
      
  def test_11_order_iter(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    olit = ri.order_iter()
    with self.assertRaises(StopIteration):
      next(olit)
      
  def test_12_order_iter(self):
    oi1 = OrderInfo('House1', 'Road2')
    oi2 = OrderInfo(14, 'Road1')
    ol = OrderList([oi1, oi2])
    ri = RoundInfo(2, 'Round2', [mhi1, mhi2], ol)
    olit = ri.order_iter()
    self.assertEqual(next(olit), oi1)
    self.assertEqual(next(olit), oi2)
    with self.assertRaises(StopIteration):
      next(olit)

  def test_13_iter(self):
    oi1 = OrderInfo('House1', 'Road2')
    oi2 = OrderInfo(14, 'Road1')
    ol = OrderList([oi1, oi2])
    ri = RoundInfo(3, 'Round3', [mhi1, mhi2], ol)
    riit = iter(ri)
    self.assertEqual(next(riit), oi1)
    self.assertEqual(next(riit), oi2)
    with self.assertRaises(StopIteration):
      next(riit)
      
  def test_14_iter(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    riit = iter(ri)
    self.assertEqual(next(riit), mhi1)
    self.assertEqual(next(riit), mhi2)
    with self.assertRaises(StopIteration):
      next(riit)
    
  def test_15_eq_01(self):
    ri = RoundInfo(1, 'Round1', [mhi1, mhi2])
    oi = OrderInfo(14, 'Road1')
    self.assertFalse(ri == oi)
    
  def test_15_eq_02(self):
    ri1 = RoundInfo(1, 'Round1', [mhi1, mhi2])
    ri2 = RoundInfo(2, 'Round1', [mhi1, mhi2])
    self.assertFalse(ri1 == ri2)
    
  def test_15_eq_03(self):
    ri1 = RoundInfo(1, 'Round1', [mhi1, mhi2])
    ri2 = RoundInfo(1, 'Round2', [mhi1, mhi2])
    self.assertFalse(ri1 == ri2)
    
  def test_15_eq_04(self):
    ri1 = RoundInfo(1, 'Round1', None)
    ri2 = RoundInfo(1, 'Round1', [mhi2])
    self.assertFalse(ri1 == ri2)
    self.assertFalse(ri2 == ri1)
    
  def test_15_eq_05(self):
    ri1 = RoundInfo(1, 'Round1', [mhi1])
    ri2 = RoundInfo(1, 'Round1', [mhi2])
    self.assertFalse(ri1 == ri2)
    
  def test_15_eq_06(self):
    oi1 = OrderInfo(14, 'Road1')
    ri1 = RoundInfo(1, 'Round1', [mhi1], None)
    ri2 = RoundInfo(1, 'Round1', [mhi1], [oi1])
    self.assertFalse(ri1 == ri2)
    self.assertFalse(ri2 == ri1)
    
  def test_15_eq_07(self):
    oi1 = OrderInfo(14, 'Road1')
    oi2 = OrderInfo(14, 'Road2')
    ri1 = RoundInfo(1, 'Round1', [mhi1], [oi1])
    ri2 = RoundInfo(1, 'Round1', [mhi1], [oi2])
    self.assertFalse(ri1 == ri2)
    
  def test_15_eq_08(self):
    oi1 = OrderInfo(14, 'Road1')
    ri1 = RoundInfo(1, 'Round1', [mhi1], [oi1])
    ri2 = RoundInfo(1, 'Round1', [mhi1], [oi1])
    self.assertTrue(ri1 == ri2)
