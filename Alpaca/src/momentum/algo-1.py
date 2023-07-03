import os
import alpaca_trade_api as tradeapi
import talib
import numpy as np

# Get Alpaca API credentials from environment variables
ALPACA_API_KEY = os.environ['ALPACA_API_KEY']
ALPACA_SECRET_KEY = os.environ['ALPACA_SECRET_KEY']

# Set up Alpaca API
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, api_version='v2')

# Define stock universe
stock_universe = ['AAPL', 'GOOG', 'MSFT', ...] # add more stock symbols as needed

# Define parameters
SMA_PERIOD = 200
RSI_PERIOD = 14
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9
MIN_OPTIONS_VOLUME = 1000
MIN_OPEN_INTEREST = 1000

# Define trading strategy
def calculate_trading_signal(data):
    # Calculate SMA
    sma = talib.SMA(data['close'], timeperiod=SMA_PERIOD)

    # Calculate RSI
    rsi = talib.RSI(data['close'], timeperiod=RSI_PERIOD)

    # Calculate MACD
    macd, macdsignal, macdhist = talib.MACD(data['close'], 
                                            fastperiod=MACD_FAST_PERIOD, 
                                            slowperiod=MACD_SLOW_PERIOD, 
                                            signalperiod=MACD_SIGNAL_PERIOD)

    # Calculate momentum
    momentum = data['close'][-1] - data['close'][0]

    # Determine trend
    if data['close'][-1] > sma[-1] and macd[-1] > macdsignal[-1]:
        trend = 'UP'
    elif data['close'][-1] < sma[-1] and macd[-1] < macdsignal[-1]:
        trend = 'DOWN'
    else:
        trend = 'FLAT'

    # Determine trade signal
    if rsi[-1] < 30 and momentum > 0 and trend == 'UP':
        signal = 'BUY'
    elif rsi[-1] > 70 and momentum < 0 and trend == 'DOWN':
        signal = 'SELL'
    else:
        signal = 'HOLD'

    return signal

# Place a trade
def place_trade(option, data, signal):
    if signal == 'BUY':
        api.submit_order(
            symbol=option.symbol,
            qty=1,
            side='buy',
            type='limit',
            time_in_force='gtc',
            limit_price=data['close'][-1]
        )
    elif signal == 'SELL':
        api.submit_order(
            symbol=option.symbol,
            qty=1,
            side='sell',
            type='limit',
            time_in_force='gtc',
            limit_price=data['close'][-1]
        )

# Main trading loop
while True:
    # Get most active stock options
    active_options = api.get_most_active_options()

    # Filter for high volume and open interest contracts
    filtered_options = [option for option in active_options if option.volume > MIN_OPTIONS_VOLUME and option.open_interest > MIN_OPEN_INTEREST]

    # Get data for selected options
    for option in filtered_options:
        data = api.get_barset(option.symbol, 'day', limit=SMA_PERIOD+1).df[option.symbol]

        # Check if there is enough data
        if len(data) == SMA_PERIOD+1:
            # Calculate trading signal
            signal = calculate_trading_signal(data)

            # Place trade
            place_trade(option, data, signal)