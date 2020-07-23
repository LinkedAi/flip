from enum import Enum

class Rotation(Enum):
  ninety = '90'
  upside_down = 'upside down'
  random = 'random'

class Position(Enum):
  percentage = 'percentage'
  random = 'random'

class Resize(Enum):
  symmetricw = 'symmetricw'
  symmetrich = 'symmetrich'
  asymmetric = 'asymmetric'

class Flip(Enum):
  x = 'x'
  y = 'y'
  random = 'random'
