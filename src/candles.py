class Candle:

  """
    Represents a candlestick in trading data. Each Candle object contains information
    about price movements and trade volume during a specific time interval.

    Attributes:
        time_start (int): The start time of the candle in milliseconds.
        time_end (int): The end time of the candle in milliseconds.
        start_price (float): The price at the beginning of the time interval.
        end_price (float): The price at the end of the time interval.
        max_price (float): The highest price within the time interval.
        min_price (float): The lowest price within the time interval.
        buy_amount (float): Total volume of assets bought in the time interval.
        sell_amount (float): Total volume of assets sold in the time interval.
        buy_average_price (float): Average price of buy transactions.
        sell_average_price (float): Average price of sell transactions.
    """

  def __init__(self, time_start, time_end, start_price, end_price, max_price, min_price,
                 buy_amount, sell_amount, buy_average_price, sell_average_price):
    self.time_start = time_start
    self.time_end = time_end
    self.start_price = start_price
    self.end_price = end_price
    self.max_price = max_price
    self.min_price = min_price
    self.buy_amount = buy_amount
    self.sell_amount = sell_amount
    self.buy_average_price = buy_average_price
    self.sell_average_price = sell_average_price