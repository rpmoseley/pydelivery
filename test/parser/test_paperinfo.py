'''
This module will test the PaperInfo object that is part of the parseround
program that will generate a database from the provided *.inp files.
'''

import unittest
from pydelivery.parser.parseround import PaperInfo

class TestPaperInfo_Init(unittest.TestCase):
  'Class that tests the initialisation of the PaperInfo object'
  def test_01_init(self):
    with self.assertRaises(TypeError) as e:
      pi = PaperInfo()
    self.assertEqual(e.exception.args[0], "__init__() missing 1 required positional argument: 'name'")
    
  def test_02_init(self):
    with self.assertRaises(TypeError) as e:
      pi = PaperInfo(None)
    self.assertEqual(e.exception.args[0], 'Must provide a name for the information')
    
  def test_03_init(self):
    with self.assertRaises(TypeError) as e:
      pi = PaperInfo('Paper', None, -2)
    self.assertEqual(e.exception.args[0], 'Must provide a positive number of copies')
    
  def test_04_init(self):
    pi = PaperInfo('Paper', None)
    self.assertEqual(pi._title, 'Paper')
    self.assertEqual(pi._days.days, {1, 2, 3, 4, 5, 6, 7})
    self.assertEqual(pi._copies, 1)
  
  def test_05_num_copies(self):
    pi = PaperInfo('Paper', None)
    with self.assertRaises(AttributeError) as e:
      pi.num_copies = -1
    self.assertEqual(e.exception.args[0], "can't set attribute")
    self.assertEqual(pi.num_copies, 1)

  def test_06_daysequence(self):
    pi = PaperInfo('Paper', None)
    with self.assertRaises(AttributeError) as e:
      pi.days = '8'
    self.assertEqual(e.exception.args[0], "can't set attribute")

  def test_07_daysequence(self):
    with self.assertRaises(KeyError) as e:
      pi = PaperInfo('Paper', {8})
    self.assertEqual(e.exception.args[0], 8)
    
  def test_08_daysequence(self):
    with self.assertRaises(ValueError) as e:
      pi = PaperInfo('Paper', '8')
    self.assertEqual(e.exception.args[0], 'Day sequence contains no valid days')
    
    
class TestPaperInfo_Oper(unittest.TestCase):
  'Class that tests the operation of the PaperInfo object'
  def test_01_add_days(self):
    pi = PaperInfo('Paper', '6')       # Add a paper delivered on Saturday
    pi.add_days('5')                   # Add a paer to be delivered on Friday
    self.assertEqual(pi.days, {5, 6})

  def test_51_add_days_fail(self):
    pi = PaperInfo('Paper', '6')
    with self.assertRaises(ValueError) as e:
      pi.add_days('9')
    self.assertEqual(e.exception.args[0], 'Day sequence contains no valid days')
    
  def test_52_add_days_fail(self):
    pi = PaperInfo('Paper', '6')
    pi.add_days('7')
    self.assertEqual(pi.days, {6, 7})
    
  def test_53_remove_days(self):
    pi = PaperInfo('Paper', '567')
    pi.remove_days('6')
    self.assertEqual(pi.days, {5, 7})
