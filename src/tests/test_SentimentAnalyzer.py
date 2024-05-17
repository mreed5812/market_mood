import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import patch, MagicMock
from src.data_analyzer.SentimentAnalyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):

    @patch('src.data_analyzer.SentimentAnalyzer.sqlite3.connect')
    @patch('src.data_analyzer.SentimentAnalyzer.TextBlob')
    def test_update_sentiment_values(self, mock_textblob, mock_connect):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Set up the cursor to return test data
        test_rows = [(1, "source", "author", "title", "description", "url", "url_to_image", "published_at", "This is a test content", "symbol", None)]
        mock_cursor.fetchall.return_value = test_rows
        
        # Mock TextBlob to return a sentiment polarity
        mock_blob_instance = MagicMock()
        mock_blob_instance.sentiment.polarity = 0.5
        mock_textblob.return_value = mock_blob_instance
        
        # Initialize SentimentAnalyzer and call the method
        analyzer = SentimentAnalyzer()
        analyzer.update_sentiment_values("symbol")
        
        # Check that the SELECT query was executed correctly
        mock_cursor.execute.assert_any_call('''SELECT * FROM news_stories WHERE symbol = ?''', ("symbol",))
        
        # Check that the UPDATE query was executed correctly
        mock_cursor.execute.assert_any_call('''UPDATE news_stories SET sentiment = ? WHERE id = ?''', (0.5, 1))
        
        # Ensure the changes were committed and the connection was closed
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
