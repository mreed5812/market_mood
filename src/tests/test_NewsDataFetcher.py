import unittest
from unittest.mock import patch, MagicMock
from src.data_collector.NewsDataFetcher import NewsDataFetcher

class TestNewsDataFetcher(unittest.TestCase):

    @patch('src.data_collector.NewsDataFetcher.ExternalNewsAPI')
    def test_get_news(self, mock_news_api):
        mock_news_api_instance = mock_news_api.return_value
        mock_news_api_instance.fetch_news.return_value = {"news": "data"}

        fetcher = NewsDataFetcher()
        result = fetcher.get_news()

        self.assertEqual(result, {"news": "data"})
        mock_news_api_instance.fetch_news.assert_called_once()

if __name__ == '__main__':
    unittest.main()
