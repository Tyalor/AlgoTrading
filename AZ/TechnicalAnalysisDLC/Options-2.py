#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from IPython.display import HTML

# Function to get filtered options data
def get_filtered_options_data(symbol, expiration_date, min_price, max_price, min_volume, min_open_interest, std_dev_filter=None):
    ticker = yf.Ticker(symbol)
    last_price = ticker.history(period="1d")['Close'].iloc[-1]
    std_dev = ticker.history(period='1y')['Close'].std()

    try:
        options_data = ticker.option_chain(expiration_date)
    except ValueError:
        return None, None

    if std_dev_filter:
        lower_bound = last_price - (std_dev * std_dev_filter)
        upper_bound = last_price + (std_dev * std_dev_filter)

    def filter_options(options_df):
        filtered_df = options_df[
            (options_df['lastPrice'] >= min_price) &
            (options_df['lastPrice'] <= max_price) &
            (options_df['volume'] >= min_volume) &
            (options_df['openInterest'] >= min_open_interest)
        ]
        if std_dev_filter:
            filtered_df = filtered_df[
                (filtered_df['strike'] >= lower_bound) &
                (filtered_df['strike'] <= upper_bound)
            ]
        return filtered_df

    filtered_calls = filter_options(options_data.calls)
    filtered_puts = filter_options(options_data.puts)

    return filtered_calls, filtered_puts

# Function to generate date range
def generate_date_range(start_date, end_date):
    if not end_date:
        return [start_date]
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
    return [date.strftime("%Y-%m-%d") for date in date_generated if date.weekday() == 4]

# Function to return HTML string
def get_formatted_table_html(df, title):
    formatted_df = df.style.set_table_styles(
        [{'selector': 'th', 'props': [('font-size', '10pt'), ('text-align', 'center')]},
         {'selector': 'td', 'props': [('text-align', 'center')]}]
    ).format(precision=2)
    return f"<h3>{title}</h3>" + formatted_df.to_html()

# Main processing function for multiple tickers
def process_tickers(tickers, dates, min_price, max_price, min_volume, min_open_interest, std_dev_filter):
    for ticker_symbol in tickers:
        for expiration_date in dates:
            print(f"\nProcessing {ticker_symbol} for expiration date: {expiration_date}")
            calls, puts = get_filtered_options_data(ticker_symbol, expiration_date, min_price, max_price, min_volume, min_open_interest, std_dev_filter)

            if calls is not None and puts is not None:
                calls_html = get_formatted_table_html(calls, f"Filtered CALLS for {ticker_symbol} - Expiration Date: {expiration_date}")
                puts_html = get_formatted_table_html(puts, f"Filtered PUTS for {ticker_symbol} - Expiration Date: {expiration_date}")

                display(HTML(calls_html))
                display(HTML(puts_html))
            else:
                print(f"No options data available for {ticker_symbol} on this date.")

# Input fields
ticker_input = input("Enter the ticker symbols separated by commas: ")
tickers = [ticker.strip() for ticker in ticker_input.split(',')]
start_date = input("Enter the start date for expiration range (YYYY-MM-DD): ")
end_date = input("Enter the end date for expiration range (YYYY-MM-DD): ")
min_price = float(input("Enter minimum option price: "))
max_price = float(input("Enter maximum option price: "))
min_volume = int(input("Enter minimum volume: "))
min_open_interest = int(input("Enter minimum open interest: "))
std_dev_filter = input("Enter standard deviation filter (1-3 or leave blank for no filter): ")
std_dev_filter = float(std_dev_filter) if std_dev_filter else None

# Generate date range and process each ticker
dates = generate_date_range(start_date, end_date)
process_tickers(tickers, dates, min_price, max_price, min_volume, min_open_interest, std_dev_filter)

