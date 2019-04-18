'''
This is the test suite for the parseround module
'''

from pydelivery.parser.parseround import HouseInfo, PaperInfo, RoundInfo
import unittest

# Define some objects to be used within the tests
pi1 = PaperInfo('Paper1')
hi1 = HouseInfo(20, 'Road1', pi1)

class TestParseRound(unittest.TestCase):
  def test_01_add_house(self):
    '''Test the addition of a house to an empty round'''
    ri = RoundInfo(1, 'Round1')
    ri.add_house(hi1)
    self.assertEqual(ri._houses, [hi1])
