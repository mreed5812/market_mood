import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Adjust the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from app import app

class TestAppIntegration(unittest.TestCase):

    @patch('app.stock_data_fetcher', new_callable=MagicMock)
    @patch('app.news_data_fetcher', new_callable=MagicMock)
    @patch('app.sentiment_analyzer', new_callable=MagicMock)
    def test_search_function(self, mock_sentiment_analyzer, mock_news_fetcher, mock_stock_fetcher):
        # Mock the behavior of the dependencies
        mock_stock_fetcher.fetch_stock_prices.return_value = [{"date": "2024-01-01", "close": 100}]
        mock_news_fetcher.fetch_news.return_value = [{"sentiment": 0.5}]
        mock_sentiment_analyzer.update_sentiment_values.return_value = None

        # Create a test client for the Flask app
        tester = app.test_client()

        # Make a POST request to the /search endpoint
        response = tester.post('/search', data=dict(search_query="AAPL"))

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_stock_fetcher.fetch_stock_prices.assert_called_once_with("AAPL")
        self.assertEqual(mock_news_fetcher.fetch_news.call_count, 2)
        mock_news_fetcher.fetch_news.assert_any_call("AAPL")
        mock_sentiment_analyzer.update_sentiment_values.assert_called_once_with("AAPL")

if __name__ == '__main__':
    unittest.main()
