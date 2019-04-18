'''
This is the test suite for the PaperList object which provides a list with added
functionality to ensure that only elements inherited from PaperInfo can be stored.
'''

import unittest
from pydelivery.parser.parseround import PaperList, PaperInfo

# Define some instances of titles for use during testing
pi1 = PaperInfo('Paper1', '345')
pi2 = PaperInfo('Paper2', '16')
pi3 = PaperInfo('Paper3', '5')

class Test_PaperList(unittest.TestCase):
  def test_01_init(self):
    'Initialise no arguments'
    pl = PaperList()
    self.assertListEqual(pl, [])
    
  def test_02_init(self):
    'Initialise an empty list'
    pl = PaperList(None)
    self.assertListEqual(pl, [])
    
  def test_03_init(self):
    for chk in ([], ()):
      with self.subTest(chk=chk):
        with self.assertRaises(ValueError) as e:
          pl = PaperList(chk)
        self.assertEqual(e.exception.args[0], "Must provide a sequence with at least one 'PaperInfo' instance")
    
  def test_04_init(self):
    for chk in ({}, dict(a=1), 'Paper1'):
      with self.subTest(chk=chk):
        with self.assertRaises(ValueError) as e:
          pl = PaperList(chk)
        self.assertEqual(e.exception.args[0], "All elements must be 'PaperInfo' instances")
        
  def test_05_append(self):
    for chk in ({}, dict(a=1), 'Paper1'):
      with self.subTest(chk=chk):
        pl = PaperList(None)
        with self.assertRaises(ValueError) as e:
          pl.append(chk)
        self.assertEqual(e.exception.args[0], "All elements must be 'PaperInfo' instances")    
    
  def test_06_append(self):
    pl = PaperList(None)
    pl.append(pi1)
    self.assertListEqual(pl, [pi1])
    
  def test_07_append(self):
    pl = PaperList(None)
    with self.assertRaises(TypeError) as e:
      pl.append(pi1, pi2, pi3)
    self.assertEqual(e.exception.args[0], "append() takes 2 positional arguments but 4 were given")
    
  def test_08_extend(self):
    pl = PaperList(None)
    pl.extend(pi1, pi2, pi3)
    self.assertListEqual(pl, [pi1, pi2, pi3])
  
  def test_09_extend(self):
    pl = PaperList(None)
    pl.extend(pi1, [pi2, pi3])
    self.assertListEqual(pl, [pi1, pi2, pi3])
    
  def test_10_getitem(self):
    pl = PaperList([pi1, pi3])
    self.assertEqual(pl[1], pi3)
    
  def test_11_getitem(self):
    pl = PaperList([pi1, pi3])
    with self.assertRaises(ValueError) as e:
      pl['Name3']
    self.assertEqual(e.exception.args[0], "Unable to find item indexed by 'Name3'")
    
  def test_12_getitem(self):
    pl = PaperList([pi1, pi3])
    with self.assertRaises(ValueError) as e:
      pl[pi2]
    self.assertEqual(e.exception.args[0], "Must pass an integer or string to use as index")

  def test_13_getitem(self):
    pl = PaperList([pi1, pi3])
    self.assertEqual(pl['Paper1'], pi1)
