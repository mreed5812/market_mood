import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import patch, MagicMock
from src.data_collector.NewsDataFetcher import NewsDataFetcher

class TestNewsDataFetcher(unittest.TestCase):

    @patch('src.data_collector.NewsDataFetcher.requests.get')
    @patch('src.data_collector.database_operations.DatabaseOperations.fetch_news_stories_by_symbol_and_date_range')
    @patch('src.data_collector.database_operations.DatabaseOperations.insert_news_stories')
    def test_fetch_news(self, mock_insert_news_stories, mock_fetch_news_stories_by_symbol_and_date_range, mock_get):
        mock_fetch_news_stories_by_symbol_and_date_range.return_value = []

        mock_response = MagicMock()
        expected_json = {
            "articles": [
                {
                    "source": {"name": "Test Source"},
                    "author": "Test Author",
                    "title": "Test Title",
                    "description": "Test Description",
                    "url": "http://test.url",
                    "urlToImage": "http://test.url/image.jpg",
                    "publishedAt": "2024-01-01T12:00:00Z",
                    "content": "Test content"
                }
            ]
        }
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fetcher = NewsDataFetcher()
        result = fetcher.fetch_news("AAPL")

        expected_result = [
            {
                "source_name": "Test Source",
                "author": "Test Author",
                "title": "Test Title",
                "description": "Test Description",
                "url": "http://test.url",
                "url_to_image": "http://test.url/image.jpg",
                "published_at": "2024-01-01",
                "content": "Test content",
                "symbol": "AAPL"
            }
        ]

        self.assertEqual(result, expected_result)
        mock_get.assert_called_once()
        mock_insert_news_stories.assert_called_once_with(expected_result, "AAPL")

if __name__ == '__main__':
    unittest.main()
