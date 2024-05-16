import unittest
from unittest.mock import patch, MagicMock
from src.data_collector.StockDataFetcher import StockDataFetcher

class TestStockDataFetcher(unittest.TestCase):

    @patch('src.data_collector.StockDataFetcher.ExternalStockAPI')
    def test_get_data(self, mock_stock_api):
        mock_stock_api_instance = mock_stock_api.return_value
        mock_stock_api_instance.fetch_data.return_value = {"stock": "data"}

        fetcher = StockDataFetcher()
        result = fetcher.get_data()

        self.assertEqual(result, {"stock": "data"})
        mock_stock_api_instance.fetch_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
