import requests
import json

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

# Iterate through all stocks in the data
for stock in data['Time Series (Daily)']:
    # Get the trading volume for the stock on the latest date
    volume = int(data['Time Series (Daily)'][stock]['6. volume'])
    
    # Get the trading volume for the stock on the previous day
    prev_volume = int(data['Time Series (Daily)'][latest_date]['6. volume'])
    
    # Calculate the percent change in trading volume between the latest date and the previous day
    pct_change = (volume - prev_volume) / prev_volume * 100
    
    # If the percent change in trading volume is greater than 100%, print the stock ticker and the percent change
    if pct_change > 100:
        print(stock, 'surged', pct_change, '% in trading volume on', latest_date)