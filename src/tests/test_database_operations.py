import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import patch, MagicMock
import src.data_collector.database_operations as db_ops

class TestDatabaseOperations(unittest.TestCase):

    @patch('src.data_collector.database_operations.sqlite3.connect')
    def test_insert_news_stories(self, mock_connect):
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Set up the cursor to return 0 for the SELECT COUNT(*) query
        mock_cursor.fetchone.return_value = [0]

        db_operations = db_ops.DatabaseOperations()
        news_stories = [
            {
                "source": {"name": "Test Source"},
                "author": "Test Author",
                "title": "Test Title",
                "description": "Test Description",
                "url": "http://test.url",
                "urlToImage": "http://test.url/image.jpg",
                "publishedAt": "2024-01-01",
                "content": "Test content"
            }
        ]
        symbol = "AAPL"
        db_operations.insert_news_stories(news_stories, symbol)

        # Print actual calls for debugging
        for call in mock_cursor.execute.call_args_list:
            print(call)

        # Verify that the connection was established
        mock_connect.assert_called_once_with(db_operations.DB_FILE_PATH)
        
        # Verify that the SELECT COUNT(*) query was executed
        select_call = '''SELECT COUNT(*) FROM news_stories WHERE source_name = ? AND published_at = ?'''
        mock_cursor.execute.assert_any_call(
            select_call, 
            ("Test Source", "2024-01-01")
        )

        # Verify that the INSERT query was executed
        insert_args = (
            "Test Source", "Test Author", "Test Title", "Test Description", 
            "http://test.url", "http://test.url/image.jpg", "2024-01-01", "Test content", "AAPL"
        )
        
        found_insert = False
        for call in mock_cursor.execute.call_args_list:
            if call[0][1] == insert_args:
                found_insert = True
                break
        self.assertTrue(found_insert, f"INSERT call not found. Calls: {mock_cursor.execute.call_args_list}")

        # Verify that the commit and close methods were called
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
