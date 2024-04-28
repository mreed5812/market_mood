import requests
from datetime import datetime, timedelta
from data import database_operations

def fetch_news(ticker):
    
    api_key = '840ef8b55d9b4dfcbe578de2860ce809'
    
    # Define the base URL for the News API
    base_url = 'https://newsapi.org/v2/everything'

    # Calculate the start date as 6 months ago from the current date
    one_month_ago = datetime.now() - timedelta(days=30*1)
    start_date = one_month_ago.strftime('%Y-%m-%d')
    print("Start Date:", start_date)  # Add this line for debugging

    # Define the parameters for the API request
    params = {
    'q': ticker,  # Search query with the ticker symbol
    'from': start_date,
    #'from': '2024-01-29',  # Start date for news search
    'sortBy': 'publishedAt',  # Sort news by publication date
    'apiKey': '840ef8b55d9b4dfcbe578de2860ce809'  # Your API key
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
        #response = requests.get('https://newsapi.org/v2/everything?q=AAPL&from=2024-03-28&sortBy=publishedAt&apiKey=840ef8b55d9b4dfcbe578de2860ce809')
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Extract the JSON data from the response
        data = response.json()

        # Extract the list of articles from the response
        articles = data.get('articles', [])

        # Insert news stories into the database
        if articles:
            database_operations.insert_news_stories(articles)

        return articles  # Return the list of news stories
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []  # Return an empty list if there's an error
