from yahoo_fin.stock_info import get_data
import yfinance as yf
import pandas as pd

# Consumer goods brands: Nike, Coca-Cola, McDonald's, P&G
tickers = 'NKE', 'KO', 'MCD', 'PG']

# Fetch the data for the last year
data = yf.download(tickers, period="1y")

# Flatten the MultiIndex columns
data.columns = ['_'.join(col).strip() for col in data.columns.values]

print(data.head())
col_names = data.columns
print(col_names)

# Save the data to an Excel file
data.to_excel('stocks_data_last_year.xlsx')