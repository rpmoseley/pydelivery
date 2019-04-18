'''
This is the test suite for the _BaseDayInfo object.
'''
from pydelivery.parser.parseround import _BaseDayInfo, DaySequence
from PySide2.QtCore import Qt
import unittest

class Test__BaseDayInfo(unittest.TestCase):
  def test_01_init(self):
    bdi = _BaseDayInfo('Name1')
    self.assertIsInstance(bdi._days, DaySequence)
    self.assertEqual(bdi.is_everyday, True)
    self.assertEqual(bdi._copies, 1)
    self.assertEqual(bdi._category, 'Newspaper')
    
  def test_02_init(self):
    bdi = _BaseDayInfo('Name1', '12')
    self.assertIsInstance(bdi._days, DaySequence)
    self.assertEqual(bdi.is_everyday, False)
    self.assertEqual(bdi.days, {Qt.DayOfWeek.Monday, Qt.DayOfWeek.Tuesday})
    self.assertEqual(bdi._copies, 1)
    self.assertEqual(bdi._category, 'Newspaper')

  def test_03_init(self):
    bdi = _BaseDayInfo('Name1', '1234567')
    self.assertEqual(bdi.is_everyday, True)
    self.assertEqual(bdi._days.days, bdi._days._def_days)
    
