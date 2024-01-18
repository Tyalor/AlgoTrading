import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from django.shortcuts import render


def index(request):
    error_message = None  # Variable to store the error message

    if request.method == 'POST':
        ticker_input = request.POST.get('tickers')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        # Check if required fields are filled
        if not (ticker_input and start_date and end_date and min_price and max_price):
            error_message = "Please fill in all required fields marked with an asterisk (*)"

        if not error_message:
            # Convert inputs safely to float or int, with defaults for empty fields
            std_dev_filter = request.POST.get('std_dev_filter')
            min_volume = request.POST.get('min_volume')
            min_open_interest = request.POST.get('min_open_interest')

            min_price = float(min_price) if min_price else 0.0
            max_price = float(max_price) if max_price else 0.0
            std_dev_filter = float(std_dev_filter) if std_dev_filter else None
            min_volume = int(min_volume) if min_volume else 0
            min_open_interest = int(min_open_interest) if min_open_interest else 0

            tickers = [ticker.strip() for ticker in ticker_input.split(',')]
            dates = generate_date_range(start_date, end_date)

            processed_data = []
            for ticker_symbol in tickers:
                ticker_data = {}
                ticker = yf.Ticker(ticker_symbol)
                last_price, timestamp, put_to_call_ratio = get_underlying_data(ticker)
                ticker_data['symbol'] = ticker_symbol
                ticker_data['last_price'] = last_price
                ticker_data['timestamp'] = timestamp
                ticker_data['put_to_call_ratio'] = put_to_call_ratio

                ticker_data['options'] = []
                for expiration_date in dates:
                    calls, puts = get_filtered_options_data(ticker_symbol, expiration_date, min_price, max_price, min_volume, min_open_interest, std_dev_filter)
                    if calls and puts:
                        ticker_data['options'].append({
                            'expiration_date': expiration_date,
                            'calls': calls,
                            'puts': puts
                        })

                processed_data.append(ticker_data)

            return render(request, 'options_app/index.html', {'data': processed_data, 'error_message': error_message})

    # For a GET request or if there's an error message, render the form
    return render(request, 'options_app/index.html', {'error_message': error_message})


# Function to get put-to-call ratio and last price of the underlying
def get_underlying_data(ticker):
    try:
        stock_data = ticker.history(period="1d")
        last_price = stock_data['Close'].iloc[-1]
        timestamp = stock_data.index[-1]
        options_data = ticker.options
        puts, calls = 0, 0
        for date in options_data:
            opt = ticker.option_chain(date)
            puts += opt.puts['openInterest'].sum()
            calls += opt.calls['openInterest'].sum()
        put_to_call_ratio = puts / calls if calls > 0 else float('inf')
        return last_price, timestamp, put_to_call_ratio
    except Exception as e:
        return None, None, None

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

    return filtered_calls.to_dict('records'), filtered_puts.to_dict('records')

# Function to generate date range
def generate_date_range(start_date, end_date):
    if not end_date:
        return [start_date]
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
    return [date.strftime("%Y-%m-%d") for date in date_generated if date.weekday() == 4]

