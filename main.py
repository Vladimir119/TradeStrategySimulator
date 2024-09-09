import pandas as pd
import os
import zipfile

from src.simulator import Simulator
from src.strategy import RandomStrategy, FuturePredictingStrategy, Strategy
from src.action import TypeCurrency, CurrencyData

def main():
    # unzip files
    zip_file_path = os.path.join('data', 'md_sim.zip')

    with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
        zip_ref.extractall('data/')

    # candle simulator
    trades_file_path = os.path.join('data', 'trades_1000pepeusdt.csv')
    trades = pd.read_csv(trades_file_path) # candles
    sim = Simulator(trades)
    sim.Build(T=3600000)
    sim.PlotAll()

    # bbo simulator
    bbo_pepeusdt_file_path = os.path.join('data', 'bbo_1000pepeusdt.csv')
    bbo_dogeusdt_file_path = os.path.join('data', 'bbo_dogeusdt.csv')
    bbo_pepeusdt = pd.read_csv(bbo_pepeusdt_file_path)
    bbo_dogeusdt = pd.read_csv(bbo_dogeusdt_file_path)

    bbo_pepeusdt = bbo_pepeusdt.sort_values(by=['local_timestamp'], ascending=True)
    bbo_dogeusdt = bbo_dogeusdt.sort_values(by=['local_timestamp'], ascending=True)

    currency_type_list = [TypeCurrency.PEPEUSDT, TypeCurrency.DOGEUSDT]
    currency_data = CurrencyData([bbo_pepeusdt, bbo_dogeusdt], currency_type_list)

    T = 1e9

    # random strategy:
    print('random strateg statistic:')
    random_strategy_actions = RandomStrategy(T, bbo_pepeusdt, currency_type_list)
    random_strategy = Strategy(random_strategy_actions, T)
    random_strategy_statistic = random_strategy.Run(currency_data, 1723248002488)
    random_strategy_statistic.print()
    random_strategy_statistic.plot()

    print('='*40 + '\n' + '='*40)

    # future predicting strategy
    print('future predicting strategy statistic:')
    future_strategy_actions = FuturePredictingStrategy(T, bbo_pepeusdt, trades ,currency_type_list)
    future_strategy = Strategy(future_strategy_actions, T)
    future_strategy_statistic = future_strategy.Run(currency_data, 1723248002488)
    future_strategy_statistic.print()
    future_strategy_statistic.plot()

if __name__ == "__main__":
    main()