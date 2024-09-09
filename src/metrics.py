import numpy as np
import matplotlib.pyplot as plt

class TradingMetrics:
  def __init__(self, pnl=0,
               traded_volume=0,
               sharp_ratio=0,
               sortino_ratio=0,
               pnl_max_drawdown=0,
               average_holding_time=0,
               number_of_position_flips=0,
               pnl_list=[0]):
    self.pnl = pnl
    self.traded_volume = traded_volume
    self.sharp_ratio = sharp_ratio
    self.sortino_ratio = sortino_ratio
    self.pnl_max_drawdown = pnl_max_drawdown
    self.average_holding_time = average_holding_time
    self.number_of_position_flips = number_of_position_flips
    self.pnl_list = pnl_list

class CurrencyMetrics:
  def __init__(self, type_currency_list):
    self.type_currency_list = type_currency_list
    self.metrics = dict()
    for type_currency in type_currency_list:
      self.metrics[type_currency] = TradingMetrics()

  def calculate(self, pnl_lists):
    for type_currency, deltha_pnl_list in pnl_lists.items():

      traded_volume = sum(abs(delta) for delta in deltha_pnl_list)

      pnl_list = np.cumsum(deltha_pnl_list).tolist()
      self.metrics[type_currency].pnl_list = pnl_list

      returns = np.diff(pnl_list) / pnl_list[1:]

      volatility = np.std(returns)

      mean_return = np.mean(returns)
      sharpe_ratio = mean_return / volatility if volatility != 0 else 0

      downside_returns = returns[returns < 0]
      downside_volatility = np.std(downside_returns) if len(downside_returns) > 0 else 0
      sortino_ratio = mean_return / downside_volatility if downside_volatility != 0 else 0

      max_drawdown = min(pnl_list)

      position_flips = 0
      for i in range(1, len(pnl_list)):
        if (pnl_list[i-1] > 0 and pnl_list[i] < 0) or (pnl_list[i-1] < 0 and pnl_list[i] > 0):
          position_flips += 1

      self.metrics[type_currency].sharp_ratio = sharpe_ratio
      self.metrics[type_currency].sortino_ratio = sortino_ratio
      self.metrics[type_currency].pnl_max_drawdown = max_drawdown
      self.metrics[type_currency].pnl = pnl_list[-1]
      self.metrics[type_currency].traded_volume = traded_volume
      self.metrics[type_currency].number_of_position_flips = position_flips

  def print(self):
    for type_currency in self.type_currency_list:
      metrics = self.metrics[type_currency]
      print(f"Currency: {type_currency}")
      print(f"PNL: {metrics.pnl}")
      print(f"Traded Volume: {metrics.traded_volume}")
      print(f"Sharp Ratio: {metrics.sharp_ratio}")
      print(f"Sortino Ratio: {metrics.sortino_ratio}")
      print(f"PNL Max Drawdown: {metrics.pnl_max_drawdown}")
      print(f"Average Holding Time: {metrics.average_holding_time}")
      print(f"Number of Position Flips: {metrics.number_of_position_flips}")
      print("-" * 40)

  def plot(self):
    # Create a plot for each currency
    for type_currency in self.type_currency_list:
        plt.plot(self.metrics[type_currency].pnl_list, label=f'{type_currency}')

    # Customize the plot
    plt.title('PnL History')
    plt.xlabel('Time')
    plt.ylabel('PnL')
    plt.legend()
    plt.show()