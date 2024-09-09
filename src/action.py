from enum import Enum

class TypeCurrency(Enum):
  PEPEUSDT=1
  DOGEUSDT=2

class CurrencyData:
  def __init__(self, data:list, type_curency_list:list):
    self.type_curency_list = type_curency_list
    self.data = dict()

    for i in range(len(data)):
      self.data[type_curency_list[i]] = data[i]

class TypeAction(Enum):
  """
    Enumeration of different types of actions that can be taken in a trading strategy.

    Enum Members:
        BUY (1): Represents a buying action.
        SELL (2): Represents a selling action.
        IGNORE (3): No action is taken.
    """
  BUY=1
  SELL=2
  IGNORE=3

class BuySellAction:
    def __init__(self, type_action:TypeAction, amount:int, type_currency:TypeCurrency):
      self.type_action = type_action
      self.amount=amount
      self.type_currency = type_currency