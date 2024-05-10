from datetime import datetime, timedelta
from . import database_operations
import requests

def fetch_news(ticker):
    # Calculate the start date as 30 days ago from the current date
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Retrieve news data from the database for the last 30 days
    news_stories = database_operations.fetch_news_stories_by_symbol_and_date_range(ticker, thirty_days_ago, datetime.now())

    # If no data is found in the database or data is not for the last 30 days, fetch from the API
    if not news_stories:
        # Make API call to fetch news data
        articles = fetch_news_from_api(ticker)
        
        # Insert news stories into the database
        if articles:
            database_operations.insert_news_stories(articles, ticker)
        
        return articles
    
    return news_stories

def fetch_news_from_api(ticker):
    api_key = '840ef8b55d9b4dfcbe578de2860ce809'
    
    # Define the base URL for the News API
    base_url = 'https://newsapi.org/v2/everything'

    # Calculate the start date as 30 days ago from the current date
    thirty_days_ago = datetime.now() - timedelta(days=30)
    start_date = thirty_days_ago.strftime('%Y-%m-%d')

    # Define the parameters for the API request
    params = {
        'q': ticker,  # Search query with the ticker symbol
        'from': start_date,
        'sortBy': 'publishedAt',  # Sort news by publication date
        'apiKey': api_key  # Your API key
    }

    # Define additional headers
    headers = {
        'Accept': 'application/json',
        'Connection': 'Upgrade'
    }

    try:
        # Send a GET request to the News API with additional headers
        user_agent = 'market mood/1.0'

        # Set the user-agent header in the request
        headers = {'User-Agent': user_agent}
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Extract the JSON data from the response
        data = response.json()

        # Extract the list of articles from the response
        articles = data.get('articles', [])
        
        for article in articles:
            # Parse the publishedAt field and format it as yyyy-mm-dd
            published_at = datetime.strptime(article.get('publishedAt', ''), '%Y-%m-%dT%H:%M:%SZ')
            article['publishedAt'] = published_at.strftime('%Y-%m-%d')
            article['symbol'] = ticker

        return articles  # Return the list of news stories
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []  # Return an empty list if there's an error
