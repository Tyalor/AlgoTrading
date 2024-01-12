import requests
import backtesting
from backtesting import Backtest, Strategy
import pandas as pd
import matplotlib.pyplot as plt
import os


# Access the API key from the environment variables
api_key = "tsvwdk7RYQVSAAtxU7Yg8ZUUnspu4dBb"

# Define the API endpoint for Forex data aggregation
forex_symbol = 'C:EURUSD'
start_date = '2022-01-09'
end_date = '2023-01-09'

url = f'https://api.polygon.io/v2/aggs/ticker/{forex_symbol}/range/1/day/{start_date}/{end_date}?unadjusted=false&sort=asc&limit=120'

# Create a dictionary with the API key as a parameter
params = {'apiKey': api_key}

# Make the GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()['results']

    # Ensure data is not empty
    if not data:
        print("Received data is empty. Exiting.")
    else:
        # Extract the OHLCV data into a Pandas DataFrame and rename the columns
        df = pd.DataFrame(
            data, columns=['t', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # Convert time to datetime
        df['t'] = pd.to_datetime(df['t'], unit='ms')

        # Clean the DataFrame by dropping rows with missing values
        df = df.dropna()

        # Check if DataFrame is not empty and contains valid data
        if df.empty or df.isna().any().any():
            print("DataFrame is empty or contains NaN values. Exiting.")
        else:
            # Define a custom strategy class for the doji strategy
            class DojiStrategy(Strategy):
                def init(self):
                    pass

                def next(self):
                    if abs(self.data.Close[0] - self.data.Close[-1]) / (self.data.High[0] - self.data.Low[0]) < 0.1:
                        self.buy()

            # Create a Backtest object with the custom strategy
            bt = Backtest(df, DojiStrategy, cash=10000)

            # Run the backtest
            stats = bt.run()

            # Print the backtest statistics
            print(stats)

            # Plot the backtest results
            bt.plot(plot_volume=True)
            plt.show()
else:
    print(
        f"Request failed with status code {response.status_code}: {response.text}")
