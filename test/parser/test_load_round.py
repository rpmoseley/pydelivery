'''
This is the test suite to check that the load_round function is working as expected
within the parseround module.
'''

import unittest
from os.path import dirname, join
from pydelivery.parser.parseround import RoundInfo, load_round

# Determine the directory in which this test is found
filedir=dirname(__file__)

class Test_LoadRound(unittest.TestCase):
  def test_01_load(self):
    ri = load_round(join(filedir, 'testround.inp'))
    self.assertIn('Round05', ri)
    self.assertIsInstance(ri['Round05'], RoundInfo)
    self.assertNotIn('NonesenseRound', ri)
