from datetime import datetime, timedelta
import requests
import logging
from . import database_operations

database_operations_instance = database_operations.DatabaseOperations()

class NewsDataFetcher:
    def __init__(self):
        self.API_KEY = '840ef8b55d9b4dfcbe578de2860ce809'
        self.BASE_URL = 'https://newsapi.org/v2/everything'

    def fetch_news(self, ticker):
        thirty_days_ago = datetime.now() - timedelta(days=29)
        news_stories = database_operations_instance.fetch_news_stories_by_symbol_and_date_range(ticker, thirty_days_ago, datetime.now())

        if not news_stories:
            articles = self.fetch_news_from_api(ticker)
            if articles:
                database_operations_instance.insert_news_stories(articles, ticker)
            return articles
        #logging.debug(f"Fetched news stories from DB: {news_stories}")
        return news_stories

    def fetch_news_from_api(self, ticker):
        params = {
            'q': ticker,
            'from': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'sortBy': 'publishedAt',
            'apiKey': self.API_KEY
        }

        headers = {'Accept': 'application/json', 'Connection': 'Upgrade', 'User-Agent': 'market mood/1.0'}

        try:
            response = requests.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            articles = data.get('articles', [])

            for article in articles:
                published_at = datetime.strptime(article.get('publishedAt', ''), '%Y-%m-%dT%H:%M:%SZ')
                article['publishedAt'] = published_at.strftime('%Y-%m-%d')
                article['symbol'] = ticker

            #logging.debug(f"Fetched news from API: {articles}")
            return articles
        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            return []
