from src.candles import Candle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.dates import date2num

class Simulator:

  def __init__(self, data):
    """
        Initializes the Simulator with the provided dataset.

        Args:
            data (pd.DataFrame): The input dataset containing historical trading data.
    """
    self.data = data.sort_values(by=['local_timestamp'], ascending=True)

  def Build(self, T:int, time_start:int=0, time_end:int=0, is_all:bool=True):
    """
        Builds and groups historical trading data into candles over time intervals.

        Args:
            T (int): The time interval in microseconds (will be converted to milliseconds).
            time_start (int): The start time to filter data (default is 0, meaning no filter).
            time_end (int): The end time to filter data (default is 0, meaning no filter).
            is_all (bool): If True, processes the entire dataset; if False, filters by time.

        Returns:
            pd.DataFrame: A DataFrame containing the grouped candle data (open, close, high, low prices, etc.).
    """
    T *= 1000 # from micro to mili
    time_start *= 1000
    time_end *= 1000

    self.T = T

    copy_data = self.data.copy()

    if not is_all:
      copy_data = copy_data[(copy_data['time_start'] >= time_start) & (copy_data['time_end'] <= time_end)]

    start_value = copy_data['local_timestamp'].min()
    copy_data['group'] = ((copy_data['local_timestamp'] - start_value) // T).astype(int)

    grouped_df = copy_data.groupby('group').agg(
        time_start=('local_timestamp', 'min'),
        time_end=('local_timestamp', 'max'),
        start_price=('price', 'first'),
        end_price=('price', 'last'),
        max_price=('price', 'max'),
        min_price=('price', 'min'),

        buy_amount=('amount', lambda x: copy_data.loc[x.index][copy_data.loc[x.index]['side'] == 'buy']['amount'].mean()),
        sell_amount=('amount', lambda x: copy_data.loc[x.index][copy_data.loc[x.index]['side'] == 'sell']['amount'].mean()),
        buy_average_price=('price', lambda x: copy_data.loc[x.index][copy_data.loc[x.index]['side'] == 'buy']['price'].mean()),
        sell_average_price=('price', lambda x: copy_data.loc[x.index][copy_data.loc[x.index]['side'] == 'sell']['price'].mean())
    )

    grouped_df = grouped_df.reset_index()

    candles = [
    Candle(row['time_start'], row['time_end'], row['start_price'], row['end_price'],
           row['max_price'], row['min_price'], row['buy_amount'], row['sell_amount'],
           row['buy_average_price'], row['sell_average_price'])
    for index, row in grouped_df.iterrows()
    ]

    cnadles_data = {
      'time_start': [candle.time_start for candle in candles],
      'time_end': [candle.time_end for candle in candles],
      'start_price': [candle.start_price for candle in candles],
      'end_price': [candle.end_price for candle in candles],
      'max_price': [candle.max_price for candle in candles],
      'min_price': [candle.min_price for candle in candles],
      'buy_amount': [candle.buy_amount for candle in candles],
      'sell_amount': [candle.sell_amount for candle in candles],
      'buy_average_price': [candle.buy_average_price for candle in candles],
      'sell_average_price': [candle.sell_average_price for candle in candles],
    }
    candles_data_df = pd.DataFrame(cnadles_data)
    self.candles_data_df = candles_data_df

  def GetCandles(self, start_time:int, end_time:int):
    return self.candles_data_df[(self.candles_data_df['time_start'] >= start_time) & (self.candles_data_df['time_end'] <= end_time)]

  def PlotAll(self, candles_size:float=4.0):
    self.Plot(self.candles_data_df, candles_size=candles_size)

  def Plot(self, candles_data, candles_size:float=4.0):
    copy_data = candles_data

    copy_data['time_start'] = pd.to_datetime(copy_data['time_start'], unit='us')
    copy_data['time_end'] = pd.to_datetime(copy_data['time_end'], unit='us')
    copy_data['time_start_num'] = copy_data['time_start'].apply(date2num)
    copy_data['time_end_num'] = copy_data['time_end'].apply(date2num)

    num_candles = len(copy_data)
    candle_width = candles_size / num_candles

    fig, ax = plt.subplots(figsize=(12, 6))

    up_color = 'green'
    down_color = 'red'

    for _, row in copy_data.iterrows():
        color = up_color if row['end_price'] > row['start_price'] else down_color
        # Draw the shadow
        ax.plot([row['time_start_num'], row['time_start_num']], [row['min_price'], row['max_price']], color='black', linestyle='-', linewidth=1)
        # Draw the body
        ax.add_patch(plt.Rectangle((row['time_start_num'] - candle_width / 2, min(row['start_price'], row['end_price'])), candle_width, abs(row['end_price'] - row['start_price']),
                                  color=color, edgecolor='black'))

    # Format the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45)

    # Set labels and title
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Candlestick Chart')

    # Show grid and plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()
