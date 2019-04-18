'''
This is the test suite for the DaySequence class within the parseround module
'''

import unittest
from pydelivery.parser.parseround import DaySequence, DayOfWeek

class TestDaySequence(unittest.TestCase):
  def test_01_init(self):
    ds = DaySequence()
    self.assertEqual(ds.days, ds._def_days)

  def test_02_init(self):
    ds = DaySequence(None)
    self.assertEqual(ds.days, ds._def_days)
    
  def test_03_init(self):
    ds = DaySequence('')
    self.assertEqual(ds.days, ds._def_days)

  def test_04_init(self):
    ds = DaySequence('1245')
    dow = DayOfWeek()
    self.assertEqual(ds.days, set([dow['Monday'], dow['Tuesday'], dow['Thursday'], dow['Friday']]))
    
  def test_05_init(self):
    ds = DaySequence('1245')
    dow = DayOfWeek()
    self.assertEqual(ds.days, {dow.Monday, dow.Tuesday, dow.Thursday, dow.Friday})
    
  def test_06_default(self):
    ds = DaySequence()
    dow = DayOfWeek()
    self.assertEqual(ds._def_days, set([dow['Monday'],   dow['Tuesday'], dow['Wednesday'],
                                        dow['Thursday'], dow['Friday'],  dow['Saturday'],
                                        dow['Sunday']]))
    self.assertEqual(len(ds.days), 7)
                     
  def test_07_days(self):
    ds = DaySequence('1234567')
    self.assertEqual(ds.days, ds._def_days)

  def test_08_days(self):
    ds = DaySequence('7654321')
    self.assertEqual(ds.days, ds._def_days)

  def test_09_days(self):
    ds = DaySequence('12654')
    self.assertEqual(ds.days, {1,2,4,5,6})

  def test_10_days_bad(self):
    ds = DaySequence('1843')
    self.assertEqual(ds.days, {1, 3, 4})
    
  def test_11_days(self):
    ds = DaySequence('MonTueSatFriThu')
    self.assertEqual(ds.days, {1,2,4,5,6})

  def test_12_days(self):
    ds = DaySequence([1,2,3,4,5,6,7])
    self.assertEqual(ds.days, ds._def_days)

  def test_13_days(self):
    ds = DaySequence({'Mon', 'Fri', 'Sun'})
    self.assertEqual(ds.days, {1, 5, 7})
    
  def test_14_days(self):
    ds = DaySequence('06')
    self.assertEqual(ds.days, {6, 7})
  
  def test_15_days(self):
    ds = DaySequence('0123456')
    self.assertEqual(ds.days, ds._def_days)
    
  def test_16_days(self):
    ds = DaySequence()
    days = ds.parse('MonFri')
    self.assertIsNotNone(days)
    self.assertEqual(days, {1, 5})
    
  def test_17_days(self):
    ds = DaySequence(4)
    
  def test_18_fail(self):
    with self.assertRaises(ValueError):
      ds = DaySequence('MoTuSaFr')
      
  def test_19_fail(self):
    with self.assertRaises(KeyError) as e:
      ds = DaySequence('MonTudWedFri')
    self.assertEqual(e.exception.args[0], 'Tud')

  def test_20_fail(self):
    with self.assertRaises(KeyError) as e:
      ds = DaySequence({5,6,8,9})
    self.assertEqual(e.exception.args[0], 8)
      
  def test_21_fail(self):
    with self.assertRaises(ValueError) as e:
      ds = DaySequence('8')
    self.assertEqual(e.exception.args[0], 'Day sequence contains no valid days')
    
  def test_22_fail(self):
    ds = DaySequence({'Mon','Tue'})
    self.assertEqual(ds.days, {1, 2})

  def test_23_embedded(self):
    ds1 = DaySequence()
    ds2 = DaySequence(ds1)
    self.assertEqual(ds2.days, ds1.days)
    
  def test_24_embedded(self):
    ds1 = DaySequence({5,6,7})
    ds2 = DaySequence(ds1)
    self.assertEqual(ds2.days, ds1.days)
    
  def test_25_add(self):
    ds1 = DaySequence({6})
    ds2 = DaySequence({5})
    ds1.add_days(ds2)
    self.assertEqual(ds1.days, {5, 6})
    
  def test_26_remove(self):
    ds1 = DaySequence({5, 6})
    ds2 = {5}
    ds1.remove_days(ds2)
    self.assertEqual(ds1.days, {6})

  def test_27_split(self):
    ds = DaySequence('2,45,7')
    self.assertEqual(ds.days, {2, 4, 5, 7})
    
  def test_28_dict(self):
    dct = dict(a=1,b=2,c=3)
    with self.assertRaises(ValueError) as e:
      ds = DaySequence(dct)
    self.assertEqual(e.exception.args[0], "Unable to handle non-iterable day sequence")
    
  def test_29_add_days(self):
    ds = DaySequence('1')
    ds.add_days('6')
    with self.assertRaises(ValueError) as e:
      ds.add_days('8')
    self.assertEqual(e.exception.args[0], "Day sequence contains no valid days")
    self.assertEqual(ds.days, {1, 6})
