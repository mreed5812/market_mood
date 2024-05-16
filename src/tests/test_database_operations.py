import unittest
from unittest.mock import patch, MagicMock
import src.data_collector.database_operations as db_ops

class TestDatabaseOperations(unittest.TestCase):

    @patch('src.data_collector.database_operations.SomeDatabaseClient')
    def test_save_data(self, mock_db_client):
        mock_db_instance = mock_db_client.return_value
        mock_db_instance.save.return_value = True

        result = db_ops.save_data({"data": "test"})
        
        self.assertTrue(result)
        mock_db_instance.save.assert_called_once_with({"data": "test"})

if __name__ == '__main__':
    unittest.main()
