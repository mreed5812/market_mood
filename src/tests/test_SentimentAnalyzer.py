import unittest
from unittest.mock import patch, MagicMock
from src.data_analyzer.SentimentAnalyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):

    @patch('src.data_analyzer.SentimentAnalyzer.ExternalSentimentAPI')
    def test_analyze(self, mock_sentiment_api):
        mock_sentiment_api_instance = mock_sentiment_api.return_value
        mock_sentiment_api_instance.analyze_text.return_value = {"sentiment": "positive"}

        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("some text")

        self.assertEqual(result, {"sentiment": "positive"})
        mock_sentiment_api_instance.analyze_text.assert_called_once_with("some text")

if __name__ == '__main__':
    unittest.main()
