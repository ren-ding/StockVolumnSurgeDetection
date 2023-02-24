import requests
import json
import datetime

# Define your API key for Alpha Vantage
API_KEY = 'API_KEY'

# Define the URL for Alpha Vantage API to retrieve daily time series data for all US stocks
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=' + API_KEY + '&outputsize=full&datatype=json'

# Send a GET request to Alpha Vantage API
response = requests.get(url)

# Parse the JSON data returned from the API
data = json.loads(response.text)

# Get the latest date available in the data
latest_date = list(data['Time Series (Daily)'].keys())[0]

# Define a dictionary to store the historical trading volume data for each stock
hist_volume = {}

# Iterate through all stocks in the data
for stock in data['Time Series (Daily)']:
    # Get the trading volume for the stock on the latest date
    volume = int(data['Time Series (Daily)'][stock]['6. volume'])
    
    # Get the trading volume for the stock on each date in the historical data
    for date in data['Time Series (Daily)']:
        if date != latest_date:
            hist_volume.setdefault(stock, []).append(int(data['Time Series (Daily)'][date]['6. volume']))
    
    # Calculate the average trading volume for the stock over the historical data
    avg_volume = sum(hist_volume[stock]) / len(hist_volume[stock])
    
    # Calculate the percent change in trading volume between the latest date and the historical average
    pct_change = (volume - avg_volume) / avg_volume * 100
    
    # If the percent change in trading volume is greater than 100%, flag the stock as having a potential surge in trading volume
    if pct_change > 100:
        print(stock, 'has a potential surge in trading volume of', pct_change, '% on', latest_date)