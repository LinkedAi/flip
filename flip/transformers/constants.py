from enum import Enum

class Position(Enum):
  percentage = 'percentage'
  random = 'random'

class Resize(Enum):
  symmetricw = 'symmetricw'
  symmetrich = 'symmetrich'
  asymmetric = 'asymmetric'