import bisect
from datetime import datetime
from src.action import TypeAction, BuySellAction, TypeCurrency
from src.metrics import CurrencyMetrics
from src.simulator import Simulator
import random

class Strategy:
  def __init__(self, actions:list, T:int):
    self.actions = actions
    self.T = T

  def Run(self, data_currency, start_time:int):
    start_time *= 1000

    random_currency_data = data_currency.data[self.actions[0][0].type_currency]
    timestamps = random_currency_data['local_timestamp'].values
    cur_time_point = start_time
    next_time_point = cur_time_point + self.T
    cur_index =  bisect.bisect_right(timestamps, cur_time_point)
    next_index =  bisect.bisect_right(timestamps, next_time_point)
    cur_datetime = datetime.utcfromtimestamp(random_currency_data['local_timestamp'].iloc[0]  / 1_000_000)

    currency_metrics = CurrencyMetrics(type_currency_list=data_currency.type_curency_list)

    pnl_lists = {instrument: [0] for instrument in data_currency.type_curency_list}

    for action_list in self.actions:
      for action in action_list:
        if action.type_action == TypeAction.IGNORE:
          continue

        cur_amount = 0
        data = data_currency.data[action.type_currency]

        deltha_money_balance = 0
        deltha_pnl = 0

        for i in range(cur_index, next_index):
          amount = 0
          if action.type_action == TypeAction.BUY:
            amount = min(action.amount - cur_amount, data.iloc[i].ask_amount)
            cur_amount += amount

            deltha_pnl -= amount * data.iloc[i].ask_price
            deltha_money_balance += amount

          else:
            amount = min(action.amount - cur_amount, data.iloc[i].bid_amount)
            cur_amount += amount

            deltha_pnl += amount * data.iloc[i].bid_price
            deltha_money_balance -= amount

          pnl_lists[action.type_currency].append(deltha_pnl)
          if amount == 0:
              break

      cur_time_point = next_time_point
      next_time_point += self.T
      cur_index =  next_index
      next_index =  bisect.bisect_right(timestamps, next_time_point)
      next_index = min(next_index, len(timestamps))

    currency_metrics.calculate(pnl_lists)
    return currency_metrics
  
def calculate_net_amount(actions, currency_type_list):
    net_amount = {instrument: 0 for instrument in currency_type_list}
    for action_list in actions:
     for action in action_list:
        if action.type_action == TypeAction.BUY:
            net_amount[action.type_currency] += action.amount  # Add for BUY
        elif action.type_action == TypeAction.SELL:
            net_amount[action.type_currency] -= action.amount  # Subtract for SELL
        # Ignore actions with TypeAction.IGNORE
    return net_amount

def RandomStrategy(T:int, data, currency_type_list)->list:
  first_value = data['local_timestamp'].iloc[0]
  last_value = data['local_timestamp'].iloc[-1]
  count_action = int((last_value - first_value) // T)
  actions = [
        [BuySellAction(
            type_action=random.choice(list(TypeAction)),
            amount=random.randint(100, 1000),
            type_currency=TypeCurrency.PEPEUSDT
        ),
         BuySellAction(
            type_action=random.choice(list(TypeAction)),
            amount=random.randint(100, 1000),
            type_currency=TypeCurrency.DOGEUSDT
        )]
        for _ in range(count_action - 1)
    ]
  return CloseStrategy(actions, currency_type_list)

def CloseStrategy(actions, currency_type_list):
  net_amount = calculate_net_amount(actions, currency_type_list)
  last_action = []
  for type_currency in net_amount:
    action = TypeAction.IGNORE
    if net_amount[type_currency] > 0:
      action = TypeAction.SELL
    elif net_amount[type_currency] < 0:
      action = TypeAction.BUY
    last_action.append(BuySellAction(action, abs(net_amount[type_currency]), type_currency))

  actions.append(last_action)
  return actions

def FuturePredictingStrategy(T:int, data, trades_data, currency_type_list)->list:
  first_value = data['local_timestamp'].iloc[0]
  last_value = data['local_timestamp'].iloc[-1]
  count_action = int((last_value - first_value) // T)

  actions = []
  sim = Simulator(trades_data)
  sim.Build(T=T//1000)

  for i in range(count_action - 1):
    candle = sim.candles_data_df.iloc[i]

    action = TypeAction.IGNORE
    if candle.end_price > candle.start_price:
      action = TypeAction.BUY
    else:
      action =TypeAction.SELL

    actions.append([BuySellAction(action, 1000, TypeCurrency.PEPEUSDT)])
  return CloseStrategy(actions, currency_type_list)
