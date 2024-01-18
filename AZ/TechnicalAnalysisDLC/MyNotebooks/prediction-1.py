import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Load stock data
stock_symbol = 'QQQ'
start_date = '2023-10-01'
end_date = '2024-01-01'
df = yf.download(stock_symbol, start=start_date, end=end_date)

# Prepare data
df = df[['Close']]
df.index = pd.to_datetime(df.index)

# Check for stationarity
adf_result = adfuller(df['Close'])
print(f'ADF Statistic: {adf_result[0]}')
print(f'p-value: {adf_result[1]}')

# Split data into training and testing sets
train_size = int(len(df) * 0.8)
train_data = df.iloc[:train_size]
test_data = df.iloc[train_size:]

# Find the optimal ARIMA parameters
auto_model = auto_arima(train_data, seasonal=False, stepwise=True, suppress_warnings=True, error_action="ignore", max_order=None, trace=True)

# Fit ARIMA model with the optimal parameters found by auto_arima
model = ARIMA(train_data, order=auto_model.order)
model_fit = model.fit()

# Forecast future stock prices
forecast_periods = 14
forecast_results = model_fit.get_forecast(steps=forecast_periods)
forecast = forecast_results.predicted_mean
conf_int = forecast_results.conf_int()

# Generate the forecast index
last_date = test_data.index[-1]
forecast_index = pd.date_range(start=last_date, periods=forecast_periods + 1, freq='B')[1:]

# Visualization
plt.figure(figsize=(14, 7))
plt.plot(test_data, label='Actual', color='blue')
plt.plot(forecast_index, forecast, label='Forecast', color='red', linestyle='--')
plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)  # Confidence intervals
plt.legend()
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title(f'Stock Price Forecast for {stock_symbol}')
plt.grid(True)
plt.show()
