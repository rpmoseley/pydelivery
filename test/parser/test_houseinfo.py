'''
This is the unittest for the HouseInfo class within the parseround module.
'''

import unittest
from pydelivery.parser.parseround import HouseInfo, PaperInfo, DaySequence, PaperList

# Create a mock instance of PaperInfo that will satisfy the checks
class Mock_PaperInfo(PaperInfo):
  def __init__(self, name, dayseq, num_copies=1):
    self._name = name
    self._dayseq = DaySequence(dayseq)
    self._copies = num_copies

class TestHouseInfo_Init(unittest.TestCase):
  'Test the initialisation of the HouseInfo object'
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo()
    self.assertEqual(e.exception.args[0], "__init__() missing 3 required positional arguments: 'name_or_number', 'road', and 'paper'")

  def test_02_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(None)
    self.assertEqual(e.exception.args[0], "__init__() missing 2 required positional arguments: 'road' and 'paper'")

  def test_03_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(None, None)
    self.assertEqual(e.exception.args[0], "__init__() missing 1 required positional argument: 'paper'")
    
  def test_04_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(None, None, None)
    self.assertEqual(e.exception.args[0], "House must be identified by a string or integer")

  def test_05_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(-2, None, None)
    self.assertEqual(e.exception.args[0], "House number should be a positive integer")
    
  def test_06_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(2, None, None)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")

  def test_07_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo('', None, None)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty house name")
    
  def test_08_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(None, 'Road', None)
    self.assertEqual(e.exception.args[0], "House must be identified by a string or integer")

  def test_09_init(self):
    hi = HouseInfo(2, 'Road', None)
    self.assertEqual(hi._titles, [])

  def test_10_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo('Special', None, None)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")

  def test_11_init(self):
    hi = HouseInfo('Special', 'Road', None)
    self.assertEqual(hi._titles, [])

  def test_12_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo(2, 2, None)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")

  def test_13_init(self):
    with self.assertRaises(TypeError) as e:
      hi = HouseInfo('Special', 2, None)
    self.assertEqual(e.exception.args[0], "Must provide a non-empty road name")

  def test_14_init(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(2, 'Road', [])
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'PaperInfo' instance")

  def test_15_init(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(2, 'Road', ())
    self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'PaperInfo' instance")
    
  def test_16_init(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(2, 'Road', {})
    self.assertEqual(e.exception.args[0], "All elements must be 'PaperInfo' instances")

  def test_17_init(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(2, 'Road', ['Telegraph'])
    self.assertEqual(e.exception.args[0], "All elements must be 'PaperInfo' instances")

  def test_18_init(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(2, 'Road', ('Telegraph',))
    self.assertEqual(e.exception.args[0], "All elements must be 'PaperInfo' instances")
    
  def test_19_init(self):
    pi = Mock_PaperInfo('Telegraph', '1234567')
    hi = HouseInfo(2, 'Road', [pi])
    self.assertEqual(hi._house, 2)
    self.assertEqual(hi._road, 'Road')
    self.assertEqual(hi._titles, [pi])
    
  def test_20_init(self):
    pi = Mock_PaperInfo('Telegraph', '1234567')
    hi = HouseInfo(2, 'Road', (pi,))
    self.assertEqual(hi._house, 2)
    self.assertEqual(hi._road, 'Road')
    self.assertEqual(hi._titles, [pi])
    
  def test_21_init(self):
    pi = Mock_PaperInfo('Telegraph', '1234567')
    hi = HouseInfo(2, 'Road', pi)
    self.assertEqual(hi._house, 2)
    self.assertEqual(hi._road, 'Road')
    self.assertEqual(hi._titles, [pi])

  def test_22_flags(self):
    pi = Mock_PaperInfo('Telegraph', '5')
    hi = HouseInfo(2, 'Road', pi, use_box=True)
    self.assertTrue('use_box' in hi.flags('4'))
    
  def test_23_iter(self):
    pi1 = Mock_PaperInfo('Paper1', '7')
    pi2 = Mock_PaperInfo('Paper2', '5')
    pi3 = Mock_PaperInfo('Paper3', '3')
    hi = HouseInfo('New', 'Road', [pi1, pi2, pi3])
    it = hi.title_iter()
    self.assertEqual(next(it), pi1)
    self.assertEqual(next(it), pi2)
    self.assertEqual(next(it), pi3)
    with self.assertRaises(StopIteration):
      self.assertEqual(next(it), None)

  def test_24_eq(self):
    hi1 = HouseInfo('Old Barn', 'Hall Lane', None)
    hi2 = HouseInfo('Old Barn', 'Hall Lane', None)
    self.assertFalse(id(hi1) == id(hi2))
    self.assertTrue(hi1 == hi2)
    
  def test_25_eq(self):
    hi1 = HouseInfo('Old Barn', 'Hall Lane', None)
    self.assertFalse(hi1 == 'Old Barn')

# Provide a simple paper for the testing
Oper_Pi = PaperInfo('Paper1', '12345')

class TestHouseInfo_Oper(unittest.TestCase):
  'Test the operation of the HouseInfo class'
  def test_50_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box=None)
    self.assertFalse(hasattr(hi, '_use_box'))
    
  def test_51_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box=True)
    self.assertEqual(hi._use_box, DaySequence())
    
  def test_52_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box=False)
    self.assertFalse(hasattr(hi, '_use_box'))
    
  def test_53_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box='')
    self.assertFalse(hasattr(hi, '_use_box'))
    
  def test_54_use_box(self):
    with self.assertRaises(ValueError) as e:
      hi = HouseInfo(20, 'Road1', Oper_Pi, use_box='8')
    self.assertEqual(e.exception.args[0], "Day sequence contains no valid days")
    
  def test_55_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box='67')
    self.assertEqual(hi._use_box, {6, 7})
    
  def test_56_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box=2)
    self.assertEqual(hi._use_box, {2})

  def test_57_use_box(self):
    hi = HouseInfo(20, 'Road1', Oper_Pi, use_box=DaySequence(2))
    self.assertEqual(hi._use_box, {2})
    
  def test_60_title_iter(self):
    pi1 = PaperInfo('Paper1', '125')
    pi2 = PaperInfo('Paper2', '135')
    pi3 = PaperInfo('Paper3', '246')
    pi4 = PaperInfo('Paper4', '157')
    hi = HouseInfo(20, 'Road1', [pi1, pi2, pi3, pi4])
    self.assertTrue(isinstance(hi._titles, list))
