'''
This program will take an input file that describes a paper round and produce the
SQL to generate a database for the paperdelivery application. It will try to read
the current list of known papers (including magazines), the seed database, and
maintain a set of known roads which are used to produce the integer values that
are stored in the application database.
'''

from collections import OrderedDict
from itertools import filterfalse

# Detail the list of objects that will be exported by default
__all__ = ('TitleMap', 'RoadMap', 'DayOfWeek', 'DaySequence', 'PaperInfo',
           'MagazineInfo', 'HouseInfo', 'OrderInfo', 'HouseList',
           'OrderList', 'PaperList', 'RoundInfo')

# Provide the mapping classes that maintain a central set of information
class _BaseMap:
  '''Class providing the shared functionality'''
  # _map should be declared in inheriting class to avoid incorrect mapping
  def __init__(self):
    if not hasattr(self, '_map'):
      # Provide a local mapping that is not shared
      self._map = OrderedDict()
    
  def _add(self, key, value, update=False, ignoredup=True):
    if key in self._map:
      if not ignoredup:
        val = self._map[key]
        if not update:
          raise ValueError("Key '{}' already present".format(key))
        elif not issubclass(type(val), type(value)):
          raise ValueError("Updating with different type: '{}' instead of '{}'".format(value.__class__.__name__, val.__class__.__name__))
        self._map[key] = value
    else:
      self._map[key] = value
      
  def _remove(self, key, error=False):
    try:
      del self._map[key]
    except KeyError:
      if error:
        raise KeyError("Key '{}' not present in mapping".format(key))
    
  def _index(self, check):
    for num, key in enumerate(self._map):
      if key == check:
        return num
    raise KeyError("Key '{}' not present in mapping".format(check))

  def __contains__(self, item):
    return item in self._map
  
  def __getitem__(self, item):
    if isinstance(item, int):
      num, keys = item, iter(self._map)
      try:
        while num >= 0:
          key = next(keys)
          num -= 1
      except StopIteration:
        raise KeyError("Element '{}' does not exist".format(item))
      return key
    elif isinstance(item, str):
      return self._map[item]
    else:
      raise ValueError('Unhandled item type for retrieval')
  
  def __setitem__(self, name, value):
    self._add(name, value)
    
  def __iter__(self):
    for key, value in self._map.items():
      yield key, value

  def numeric_iter(self):
    '''Return the list of keys in order togeather with a unique ID'''
    for num, key in enumerate(self._map):
      yield num, key


class _IncrMap(_BaseMap):
  '''Class adding increment and decrement to a _BaseMap object'''
  def _incr(self, key):
    '''Increment the value that is associated with the given KEY'''
    val = 0 if key not in self._map else self._map[key]
    if not isinstance(val, int):
      raise ValueError("Key '{}' value must be an integer".format(key))
    self._map[key] = val + 1 

  def _decr(self, key, autoremove=False, error=False):
    '''Decrement the value that is associated with the given KEY'''
    if key in self._map:
      val = self._map[key]
      if not isinstance(val, int):
        raise ValueError("Key '{}' value must be an integer".format(key))
      elif val < 1:
        if error:
          raise ValueError("Key '{}' cannot be negative".format(key))
        return val
      if autoremove and val < 2:
        del self._map[key]
      else:
        self._map[key] = val - 1
    elif error:
      raise ValueError("Key '{}' not present in mapping".format(key))

  def __setitem__(self, key, value):
    '''Set the given key incrementing the current value'''
    self._incr(key)

  def increment(self, key):
    '''Add key to map maintaining count of additions'''
    self._incr(key)
    
  def decrement(self, key, error=False):
    '''Remove a key from the map updating the count'''
    self._decr(key, autoremove=True, error=error)
    

class TitleMap(_BaseMap):
  '''Class providing the title mapping, with the added function that will prioritise
     papers above/below/with magazines
  '''
  _map = OrderedDict()
  _valid_mag_order = ('after_paper', 'before_paper', 'inwith_paper')
  
  def __init__(self, mag_order='after_paper'):
    if mag_order not in self._valid_mag_order:
      raise TypeError("Invalid magazine order given")
    self._order = list() if mag_order != 'inwith_paper' else None
    self._magorder = mag_order
    
  def add(self, name, dayseq=None, update=False):
    self._add(name, dayseq, update=update, ignoredup=False)

  def remove(self, name, error=None):
    self._remove(name, error=error)

  def index(self, name):
    return self._index(name)


class RoadMap(_IncrMap):
  '''Class providing the road mapping, maintaining count of houses on each road in mapping'''
  def add(self, house):
    '''Add a new road or incrment the number of houses on an existing one'''
    if isinstance(house, HouseInfo):
      self._incr(house._road)
    else:
      raise ValueError('Must pass an instance of HouseInfo')
  
  def remove(self, house, error=False):
    '''Remove a house from a road, removing the road if no houses remain'''
    if isinstance(house, HouseInfo):
      self._decr(house._road, autoremove=True, error=error)
    else:
      raise ValueError('Must pass an instance of HouseInfo')


# TODO Add alternative implementation not dependant on PySide2
from PySide2.QtCore import Qt

class DayOfWeek:
  '''Class providing the days of the week that is based on the
     PySide2.QtCore.Qt.DayOfWeek object, adding the ability to
     refer to the days as a number in the range 0..7, with Sunday 
     being refered by both numbers 0 and 7.
  '''
  _dow_dict = None
  _dow_names = None
  
  def __init__(self):
    if not hasattr(self, '_dow_dict') or self._dow_dict is None:
      self._dow_dict = dict()
      self._dow_dict.update(Qt.DayOfWeek.values)
      self._dow_dict[0] = self._dow_dict['0'] = self._dow_dict['Sun'] = self._dow_dict['Sunday']
      self._dow_dict[1] = self._dow_dict['1'] = self._dow_dict['Mon'] = self._dow_dict['Monday']
      self._dow_dict[2] = self._dow_dict['2'] = self._dow_dict['Tue'] = self._dow_dict['Tuesday']
      self._dow_dict[3] = self._dow_dict['3'] = self._dow_dict['Wed'] = self._dow_dict['Wednesday']
      self._dow_dict[4] = self._dow_dict['4'] = self._dow_dict['Thu'] = self._dow_dict['Thursday']
      self._dow_dict[5] = self._dow_dict['5'] = self._dow_dict['Fri'] = self._dow_dict['Friday']
      self._dow_dict[6] = self._dow_dict['6'] = self._dow_dict['Sat'] = self._dow_dict['Saturday']
      self._dow_dict[7] = self._dow_dict['7'] = self._dow_dict['Sunday']
      self._dow_names = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

  def days(self):
    'Return the days of the week'
    yield Qt.DayOfWeek.Monday
    yield Qt.DayOfWeek.Tuesday
    yield Qt.DayOfWeek.Wednesday
    yield Qt.DayOfWeek.Thursday
    yield Qt.DayOfWeek.Friday
    yield Qt.DayOfWeek.Saturday
    yield Qt.DayOfWeek.Sunday

  def __getitem__(self, dow):
    return self._dow_dict[dow]
          
  def __contains__(self, dow):
    return dow in self._dow_dict

  @property
  def Monday(self):
    return Qt.DayOfWeek.Monday
  
  @property
  def Tuesday(self):
    return Qt.DayOfWeek.Tuesday
  
  @property
  def Wednesday(self):
    return Qt.DayOfWeek.Wednesday
  
  @property
  def Thursday(self):
    return Qt.DayOfWeek.Thursday
  
  @property
  def Friday(self):
    return Qt.DayOfWeek.Friday
  
  @property
  def Saturday(self):
    return Qt.DayOfWeek.Saturday
  
  @property
  def Sunday(self):
    return Qt.DayOfWeek.Sunday
  

class DaySequence:
  '''Class providing the day sequence handling which ensures that days of the
     week are kept in ISO order, (Monday=1).

     The class will accept day sequences in the following formats:

       - a sequence or string comprising the days as the digits 1 to 7, with Sunday being 7;
       - a sequence or string comprising the days as the digits 0 to 6, with Sunday being 0;
       - a sequence or string comprising the days in full seperated by commas;
       - a sequence or string comprising the short days seperated by commas. 
  '''
  # Provide a default of all days
  _dow = DayOfWeek()
  _def_days = set(_dow.days())
  
  def __init__(self, days=None):
    self.days = self.parse(days) if days else self._def_days  
  
  def parse(self, dayseq):
    '''Handle the days string which can either be a sequence of digits from 1 to 7,
       (Monday is 1), or alternatively a sequence of the first three characters of
       the day in the local locale.
    '''
    # Convert the day sequence in a list
    if isinstance(dayseq, DaySequence):
      # Copy the day sequence from another instance
      return dayseq.days.copy()
    elif isinstance(dayseq, str):
      # Convert a string of days into a list of days
      if dayseq.find(',') > 0:
        _dayseq = list()
        for curday in dayseq.split(','):
          if len(curday) > 1:
            for chkday in curday:
              if '0' <= chkday <= '7':
                _dayseq.append(chkday)
          elif '0' <= curday <= '7':
            _dayseq.append(curday)
      elif dayseq[0].isdigit():
        _dayseq = [num for num in dayseq if '0' <= num <= '7']
      elif len(dayseq) % 3 == 0:
        _dayseq = [dayseq[num:num+3] for num in range(0, len(dayseq), 3)]
      else:
        raise ValueError('Unable to handle day sequence')
    elif isinstance(dayseq, int):
      _dayseq = [dayseq]
    elif isinstance(dayseq, (tuple, list, set)):
      _dayseq = dayseq
    else:
      raise ValueError('Unable to handle non-iterable day sequence')

    # Process each element of the list in turn.
    days = set()
    for curday in _dayseq:
      if isinstance(curday, (int, str)):
        days.add(self._dow[curday])
    
    # Check that there is at least one day in the resultant set
    if not days:
      raise ValueError('Day sequence contains no valid days')
    
    # Return the default dow set if all days were parsed
    return days if len(days) != 7 else self._def_days

  def add_days(self, dayseq):
    'Add the given day sequence to the current day sequence'
    self.days.update(self.parse(dayseq))
    
  def remove_days(self, dayseq):
    'Remove the given day sequence from the current day sequence'
    self.days.difference_update(self.parse(dayseq))
    
  def __eq__(self, other):
    'Check whether two DaySequence objects have the same days'
    if isinstance(other, DaySequence):
      return self.days == other.days
    else:
      ods = DaySequence(other)
      return self.days == ods.days


class _BaseDayInfo:
  '''Class providing shared functionality'''
  def __init__(self, name, dayseq=None, num_copies=1, category=None):
    # Validate the arguments
    if not isinstance(name, str) or name == '':
      raise TypeError('Must provide a name for the information')
    _days = DaySequence(dayseq)
    if num_copies < 1:
      raise TypeError('Must provide a positive number of copies')
    
    # Store the information for use later
    self._title = name
    self._days = _days
    self._copies = num_copies
    self._category = category or 'Newspaper'
    
  def add_days(self, days):
    'Add a sequence of days to the current days'
    self._days.add_days(days)
    
  def remove_days(self, days):
    'Remove a sequence of days from the current days'
    self._days.remove_days(days)
    
  @property
  def days(self):
    return self._days.days

  @property
  def num_copies(self):
    return self._copies
  
  @property
  def is_everyday(self):
    '''Return whether delivery is everyday'''
    return self._days.days is self._days._def_days   # TODO Check if this true
  
  
class PaperInfo(_BaseDayInfo):
  '''Class representing an individual paper'''
  def __init__(self, name, dayseq=None, num_copies=1):
    super().__init__(name, dayseq, num_copies=num_copies, category='Newspaper')


class MagazineInfo(_BaseDayInfo):
  '''Class representing an individual magazine'''
  def __init__(self, name, dayseq, frequency=None):
    super().__init__(name, dayseq, num_copies=1, category='Magazine')
    self._frequency = frequency or "W"


class HouseInfo:
  '''Class representing a house within a round'''
  def __init__(self, name_or_number, road, paper, use_box=None):
    # Validate the arguments
    if isinstance(name_or_number, int):
      if name_or_number < 1:
        raise TypeError('House number should be a positive integer')
    elif isinstance(name_or_number, str):
      if not name_or_number:
        raise TypeError('Must provide a non-empty house name')
    else:
      raise TypeError('House must be identified by a string or integer')
    
    if not isinstance(road, str) or not road:
      raise TypeError('Must provide a non-empty road name')
    
    # Store the information for use later
    self._house = name_or_number
    self._road = road
    self._titles = PaperList(paper)
    if use_box:
      if isinstance(use_box, bool):
        if use_box == True:
          self._use_box = DaySequence()
      else:
        self._use_box = DaySequence(use_box)

  def __eq__(self, other):
    '''Check if this instance matches the other instance'''
    if not isinstance(other, HouseInfo):
      return False
    return self._house == other._house and self._road == other._road
  
  def flags(self, dayseq=None):
    '''Return the current flags for the given day sequence'''
    return 'use_box' if hasattr(self, '_use_box') else None # TODO Implement a more correct solution
  
  def title_iter(self):
    '''Generator returning each of the paperinfo entries for house'''
    for paper in self._titles:
      yield paper
      

class OrderInfo:
  '''Class representing an entry in the order of a round'''
  def __init__(self, name_or_number, road):
    # Validate the arguments
    if not isinstance(name_or_number, (str, int)):
      raise TypeError('House must be identified by a string or integer')
    elif isinstance(name_or_number, int):
      if name_or_number < 1:
        raise TypeError('House number should be a positive integer')
    elif isinstance(name_or_number, str):
      if not name_or_number:
        raise TypeError('Must provide a non-empty house name')
    if not isinstance(road, str) or not road:
      raise TypeError('Must provide a non-empty road name')
    
    # Store the information for use later
    self._house = name_or_number
    self._road = road


class _LimitList(list):
  '''Mixin providing extra functionality over a normal list object,
     which limits the addition of elements to a particular instance
     of object and adds comparison that checks each element.'''
  def __init__(self, type_, name, elems=None):
    self._type = type_
    self._name = name
    
    # Invoke the actual initialiser
    super().__init__()
    if isinstance(elems, (tuple, list)):
      self.extend(elems)
    elif elems is not None:
      self.append(elems)
    
  def _all(self, elems, except_=ValueError, _flatten=True):
    '''Check if any elements are not of the correct type for this instance'''
    act_elems = self._flatten(elems, except_=except_) if _flatten else elems
    if not act_elems and except_:
      raise except_("Must provide a sequence with at least one '{}' instance".format(self._name))
    if any([not isinstance(elem, self._type) for elem in act_elems]):
      if except_:
        raise except_("Must provide a sequence of '{}' instances".format(self._name))
      return None
    return act_elems
    
  def _flatten(self, elems, except_=None, _res_elems=None):
    '''Flatten the elements into a single sequence of elements'''
    if _res_elems is None:
      _res_elems = list()
    if isinstance(elems, self._type):
      _res_elems.append(elems)
    else:
      for elem in elems:
        if isinstance(elem, (tuple, list)):
          self._flatten(elem, except_=except_, _res_elems=_res_elems)
        elif isinstance(elem, self._type):
          _res_elems.append(elem)
        elif except_:
          raise except_("All elements must be '{}' instances".format(self._name))
    return _res_elems
      
  def append(self, elem):
    '''Perform an append of a single object controlled by this instance'''
    if not isinstance(elem, self._type):
      raise ValueError("All elements must be '{}' instances".format(self._name))
    super().append(elem)
    
  def extend(self, *elems):
    '''Perform an extend of a sequence of objects controlled by this instance'''
    super().extend(self._all(elems, except_=ValueError))
    
  def __iadd__(self, elems):
    '''Perform an inline append of the given elements of type controlled by this instance'''
    super().extend(self._all(elems, except_=ValueError))
    return self
  
  def remove(self, elems):
    '''Remove the given element(s) of the correct type for this instance'''
    for elem in self._all(elems, except_=ValueError):
      super().remove(elem)
    return self

  def insert(self, index, element):
    '''Insert the given element of the correct type for this instance'''
    if isinstance(element, (list, tuple)) or not isinstance(element, self._type):
      raise ValueError("Must pass a single instance of '{}'".format(self._name))
    super().insert(index, element)
    
  def __contains__(self, elems):
    '''Perform a check if all elements are present in the associated list'''
    act_elems = self._all(elems, except_=ValueError)
    for elem in act_elems:
      if not super().__contains__(elem):
        return False
    return True
      
  def __eq__(self, other):
    '''Check if both objects are of the correct instance and elements are also correct'''
    if len(self) != len(other):
      return False
    for selem, oelem in zip(self, other):
      if not isinstance(selem, self._type) or not isinstance(oelem, self._type):
        return False
      if selem != oelem:
        return False
    return True  

    
class HouseList(_LimitList):
  '''Class providing a list limited to instances of HouseInfo'''
  def __init__(self, houses=None):
    super().__init__(HouseInfo, 'HouseInfo', houses)

  def __getitem__(self, house):
    if isinstance(house, HouseInfo):
      for item in self:
        if house == item:
          return item
    elif isinstance(house, int):
      for item in self:
        if house == 0:
          return item
        house -= 1
    else:
      raise ValueError("Must pass either an integer or instance of 'HouseInfo'")
    return None

    
class OrderList(_LimitList):
  '''Class providing a list limited to instances of OrderInfo'''
  def __init__(self, orders=None):
    super().__init__(OrderInfo, 'OrderInfo', orders)
    

class PaperList(_LimitList):
  '''Class providing a list limited to instances of _BaseDayInfo'''
  def __init__(self, papers=None):
    super().__init__(_BaseDayInfo, 'PaperInfo', papers)
      
  def __getitem__(self, name_or_number):
    '''Retrieve an element by index or name'''
    if isinstance(name_or_number, int):
      return super().__getitem__(name_or_number)
    elif isinstance(name_or_number, str):
      for item in self:
        if item._title == name_or_number:
          return item
      raise ValueError("Unable to find item indexed by '{}'".format(name_or_number))
    else:
      raise ValueError("Must pass an integer or string to use as index")

      
class RoundInfo:
  '''Class representing an entire round'''
  _max_round = 5     # Specifies the maximum number of unique rounds
  def __init__(self, number, name, houses=None, order=None):
    # Validate the arguments to ensure no bad data is passed
    if not isinstance(number, int):
      raise TypeError('Must provide a number for the round')
    elif number < 0:
      raise TypeError('Must provide a positive number for round')
    elif hasattr(self, '_max_round') and number > self._max_round:
      raise TypeError('Attempt to use round above maximum allowed')
    if not isinstance(name, str) or not name:
      raise TypeError('Must provide a name for the round')
    
    # Store the information for processing later
    self._number = number
    self._name = name
    self._houses = houses if isinstance(houses, HouseList) else HouseList(houses)
    
    # TODO Need to add code to validate the order of houses against those taking deliveries
    if order is None:
      self._order = order
    else:
      self._order = order if isinstance(order, OrderList) else OrderList(order)
  
  def house_iter(self):
    '''Generator providing the houses within this round'''
    for house in self._houses:
      yield house
      
  def order_iter(self):
    '''Generator providing the order of houses in this round'''
    if self._order:
      for order in self._order:
        yield order
    else:
      return None
      
  def __iter__(self):
    '''Provide an iterator over the houses on this round'''
    return self.order_iter() if self._order else self.house_iter()
  
  def __eq__(self, other):
    '''Compare the attributes of both objects to see if they are equal'''
    if not isinstance(other, self.__class__):
      return False
    if self._number != other._number:
      return False
    if self._name != other._name:
      return False
    if not self._houses and other._houses:
      return False
    if self._houses and not other._houses:
      return False
    if self._houses != other._houses:
      return False
    if not self._order and other._order:
      return False
    if self._order and not other._order:
      return False
    if self._order != other._order:
      return False
    return True
  
  def add_house(self, house, order=None):
    '''Add a house to the current round, unless it is already present'''
    # Validate the house
    if not isinstance(house, HouseInfo):
      raise ValueError('Can only add instances of HouseInfo')
    
    # Check if house is already present within the round
    if house in self._houses:
      raise ValueError('House is already present in round')
  
    # Check if the order, if provided, is valid
    if isinstance(order, OrderInfo):
      pass    # TODO Implement ordering of houses
      
    # Add to the list of internal list of houses
    self._houses.append(house)

  def rem_house(self, house):    
    '''Remove a house from the current round, unless it is not present'''
    # Validate the house
    if not isinstance(house, HouseInfo):
      raise ValueError('Can only remove instances of HouseInfo')
    
    # Check if house not present within the round
    if house not in self._houses:
      raise ValueError('House not present in round')
    
    # Remove from the list of houses
    self._houses.remove(house)

    
# Provide some specialisations for known papers or magazines
HasStandard = PaperInfo('Standard', '5')
HasStandard2 = PaperInfo('Standard', '5', num_copies=2)

# Function to load an input file and return an instance of the round information
_Round_locals = dict(RoundInfo    = RoundInfo,
                     HouseList    = HouseList,    HouseInfo    = HouseInfo,
                     PaperList    = PaperList,    PaperInfo    = PaperInfo,
                     OrderList    = OrderList,    OrderInfo    = OrderInfo,
                     MagazineInfo = MagazineInfo,
                     HasStandard  = HasStandard,  HasStandard2 = HasStandard2,
                    )

def load_round(name):
  '''Load the round information with a restricted list of objects, then tidy up.'''
  
  # Load the round information from the given NAME file
  with open(name, 'rt') as fd:
    code = fd.read()
    
  # Create a new namespace from a copy of the locals dictionary
  round_dict = _Round_locals.copy()
  exec(code, globals(), round_dict)
  
  # Mark the original locals to be removed from the dictionary
  rem_name = set(_Round_locals)
  
  # Add any items that are not RoundInfo instances
  for name in round_dict:
    if not isinstance(round_dict[name], RoundInfo):
      rem_name.add(name)
      
  # Remove the items which correspond to the remembered names
  for name in rem_name:
    del round_dict[name]

  # Return the resultant dictionary of RoundInfo objects
  return round_dict
