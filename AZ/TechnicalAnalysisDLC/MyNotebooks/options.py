from datetime import datetime as dt  # Import datetime class as dt
import pandas as pd
import matplotlib.pyplot as plt
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange

def create_signals(ticker, exp_date, client):
    transactions = {
        "transaction_date": [],
        "ticker": [],
        "strike": [],
        "exp_date": [],
        "transaction_type": [],
    }

    strikes = client.get_strikes(ticker, exp_date)
    for strike in strikes:
        try:
            data = client.get_hist_option(
                req=OptionReqType.EOD,
                root=ticker,
                exp=exp_date,
                strike=strike,
                right=OptionRight.CALL, 
                date_range=DateRange(exp_date - dt.timedelta(days=90), exp_date)
            )
            print(data)
        except:
            continue

# client = ThetaClient(launch=False)
client = ThetaClient(username="tyalorkny@gmail.com", passwd=open("passwd.txt", "r").read())

# with client.connect():
#     ticker = "BMY"
#     exp_dates = client.get_expirations(ticker)

#     for exp_date in exp_dates[390:400]:
#         try:
#             create_signals(ticker, exp_date, client)
#         except Exception as e:
#             # continue
#             print(str(e))
        

with client.connect():  # Make any requests for data inside this block. Requests made outside this block wont run.
    data = client.get_hist_option(
          req=OptionReqType.EOD,
          root="AAPL",
          exp=dt(2022, 11, 25),
          strike=150,
          right=OptionRight.CALL,
          date_range=DateRange(dt(2022, 10, 15), dt(2022, 11, 15))
    )
    print(data)
