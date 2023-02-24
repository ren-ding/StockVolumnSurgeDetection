import requests
import json
import datetime
import tweepy

# Define your API keys for News API and Tweepy
NEWS_API_KEY = 'NEWS_API_KEY'
TWITTER_CONSUMER_KEY = 'TWITTER_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET = 'TWITTER_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN = 'TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'TWITTER_ACCESS_TOKEN_SECRET'

# Define the URL for News API to search for news articles containing a stock symbol
news_url = 'https://newsapi.org/v2/everything'

# Define the parameters for News API search
news_params = {
    'apiKey': NEWS_API_KEY,
    'q': '',
    'sortBy': 'publishedAt',
    'language': 'en'
}

# Authenticate with Tweepy API
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define the search query for Tweepy API to search for tweets containing a stock symbol
tweet_query = ''

# Define a dictionary to store the number of news articles and tweets mentioning each stock
mentions = {}

# Define a list of flagged stocks
flagged_stocks = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'FB']

# Define the threshold for a significant increase in mentions or news articles
threshold = 50

# Define the time interval for monitoring news and social media feeds in seconds
interval = 300

while True:
    # Iterate through all flagged stocks
    for stock in flagged_stocks:
        # Update the search parameters for News API and Tweepy API
        news_params['q'] = stock
        tweet_query = stock
        
        # Send a GET request to News API
        news_response = requests.get(news_url, params=news_params)
        
        # Parse the JSON data returned from News API
        news_data = json.loads(news_response.text)
        
        # Count the number of news articles mentioning the stock in the last 24 hours
        num_news = 0
        for article in news_data['articles']:
            published_at = datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            if datetime.datetime.utcnow() - published_at <= datetime.timedelta(days=1):
                num_news += 1
        
        # Send a search query to Tweepy API
        tweets = api.search(q=tweet_query, count=100, lang='en')
        
        # Count the number of tweets mentioning the stock in the last 24 hours
        num_tweets = 0
        for tweet in tweets:
            if tweet.created_at >= (datetime.datetime.now() - datetime.timedelta(days=1)):
                num_tweets += 1
        
        # If the number of news articles or tweets mentioning the stock is significantly greater than the threshold, flag the stock as having a surprise event affecting it
        if num_news >= threshold or num_tweets >= threshold:
            mentions[stock] = (num_news, num_tweets)
            print(stock, 'has a surprise event affecting it:', mentions[stock])
    
    # Wait for the specified time interval before checking again
    time.sleep(interval)