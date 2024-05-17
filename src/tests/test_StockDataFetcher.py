import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import patch, MagicMock
from src.data_collector.StockDataFetcher import StockDataFetcher

class TestStockDataFetcher(unittest.TestCase):

    @patch('src.data_collector.StockDataFetcher.requests.get')
    def test_fetch_stock_data(self, mock_get):
        mock_response = MagicMock()
        expected_json = {
            "Time Series (Daily)": {
                "2024-01-01": {
                    "1. open": "100.0",
                    "2. high": "110.0",
                    "3. low": "90.0",
                    "4. close": "105.0",
                    "5. volume": "1000"
                }
            }
        }
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fetcher = StockDataFetcher()
        result = fetcher.fetch_stock_data("AAPL")

        expected_result = [
            {
                'symbol': "AAPL",
                'date': "2024-01-01",
                'open': 100.0,
                'high': 110.0,
                'low': 90.0,
                'close': 105.0,
                'volume': 1000
            }
        ]
        self.assertEqual(result, expected_result)
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
