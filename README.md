# Cryptocurrency Trading Strategy Simulator

This project is designed to simulate and backtest cryptocurrency trading strategies using real-time and historical market data for assets like 1000PEPEUSDT and DOGEUSDT. The simulation uses both Best Bid Offer (BBO) and trades data to evaluate different strategies and their performance metrics.

## How the Project Works

The project is structured to process historical market data (BBO and trades) to backtest and analyze the performance of various trading strategies. The process generally follows these steps:

1. **Data Loading:**  
   Market data is loaded from the `data/` directory in CSV format. This includes both Best Bid Offer (BBO) and trade data for different cryptocurrency pairs (e.g., 1000PEPEUSDT, DOGEUSDT).

2. **Candlestick Generation:**  
   The raw data is converted into candlestick (OHLCV) format using the `candles.py` script. This step is critical for applying certain technical indicators.

3. **Strategy Definition:**  
   Trading strategies are defined in the `strategy.py` file. These strategies make decisions based on market data and signal when to enter or exit a trade.

4. **Simulation:**  
   The `simulator.py` file runs the trading strategies against the historical data. It simulates trading operations, including order placement and execution based on the strategies.

5. **Actions and Orders:**  
   The `action.py` file manages the execution of trades, determining how buy/sell orders are placed, and ensuring they conform to the strategy’s logic.

6. **Metrics and Performance Evaluation:**  
   After a strategy completes its simulation, performance metrics such as profit/loss, drawdown, and Sharpe ratio are calculated using functions from the `metrics.py` file.

## Installation

### Prerequisites

- Python 3.10+
- Required libraries (you can install them using `pip`):

```bash
pip install -r requirements.txt
```

### Project Setup
1. Clone this repository:
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```
### Usage
To run a simulation or backtest a trading strategy, you can execute the ```main.py``` script: 
```bash
python main.py
```
This will trigger the trading simulation process, using the defined strategies and data in the data/ folder.

You can modify or create new strategies by editing the strategy.py file, and adjust the simulation parameters in simulator.py.



