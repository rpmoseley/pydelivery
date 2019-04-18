'''
This test suite will check that the DayOfWeek object is working as expected
'''

import unittest
from pydelivery.parser.parseround import DayOfWeek
from PySide2.QtCore import Qt

class TestDayOfWeek(unittest.TestCase):
  def test_01_init(self):
    dow = DayOfWeek()
    for day, info in (('Monday', Qt.DayOfWeek.Monday),
                      ('Tuesday', Qt.DayOfWeek.Tuesday),
                      ('Wednesday', Qt.DayOfWeek.Wednesday),
                      ('Thursday', Qt.DayOfWeek.Thursday),
                      ('Friday', Qt.DayOfWeek.Friday),
                      ('Saturday', Qt.DayOfWeek.Saturday),
                      ('Sunday', Qt.DayOfWeek.Sunday)):
      with self.subTest(day=day, info=info):
        self.assertEqual(dow._dow_dict[day], info)
    self.assertEqual(dow._dow_names, set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))

  def test_02_init(self):
    dow = DayOfWeek()
    self.assertEqual(dow.Monday, Qt.DayOfWeek.Monday)
    self.assertEqual(dow.Tuesday, Qt.DayOfWeek.Tuesday)
    self.assertEqual(dow.Wednesday, Qt.DayOfWeek.Wednesday)
    self.assertEqual(dow.Thursday, Qt.DayOfWeek.Thursday)
    self.assertEqual(dow.Friday, Qt.DayOfWeek.Friday)
    self.assertEqual(dow.Saturday, Qt.DayOfWeek.Saturday)
    self.assertEqual(dow.Sunday, Qt.DayOfWeek.Sunday)
    
  def test_03_int(self):
    dow = DayOfWeek()
    for num in range(8):
      with self.subTest(num=num):
        self.assertEqual(dow[num], dow._dow_dict[num])

  def test_04_str(self):
    dow = DayOfWeek()
    for day in dow.days():
      with self.subTest(day=day.name):
        self.assertEqual(dow[day], dow._dow_dict[day])

  def test_05_bad_int(self):
    dow = DayOfWeek()
    with self.assertRaises(KeyError):
      dow[9]

  def test_06_bad_str(self):
    dow = DayOfWeek()
    with self.assertRaises(KeyError):
      dow['Sundat']
      
  def test_07_bad_obj(self):
    dow = DayOfWeek()
    with self.assertRaises(TypeError):
      dow[{'Mon'}]

  def test_08_set_bad(self):
    dow = DayOfWeek()
    with self.assertRaises(TypeError):
      dow['Noneday'] = None

  def test_09_sunday(self):
    dow = DayOfWeek()
    self.assertEqual(dow[0], Qt.DayOfWeek.Sunday)
    self.assertEqual(dow[7], Qt.DayOfWeek.Sunday)
    
  def test_10_contains(self):
    dow = DayOfWeek()
    self.assertEqual('Monday' in dow, True)
