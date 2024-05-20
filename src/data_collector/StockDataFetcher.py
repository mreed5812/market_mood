from datetime import datetime, timedelta
import requests
import logging


class StockDataFetcher:
    def __init__(self):
        self.API_KEY = 'SFRHBUTCXB3RDG5S'
        # Import database_operations here to avoid circular import
        from . import database_operations
        self.database_operations_instance = database_operations.DatabaseOperations()

    def fetch_stock_data(self, symbol):
        # Log the current datetime module to ensure it's in scope
        logging.debug(f"Current datetime module: {datetime}")

        one_month_ago = datetime.now() - timedelta(days=30*1)
        start_date = one_month_ago.strftime('%Y-%m-%d')

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.API_KEY}&outputsize=compact&datatype=json&startdate={start_date}'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            data = response.json()
            if 'Time Series (Daily)' in data:
                stock_prices = []
                for date, values in data['Time Series (Daily)'].items():
                    stock_prices.append({
                        'symbol': symbol,
                        'date': date,
                        'open': float(values['1. open']),
                        'high': float(values['2. high']),
                        'low': float(values['3. low']),
                        'close': float(values['4. close']),
                        'volume': int(values['5. volume'])
                    })
                logging.debug(f"Fetched stock data")
                return stock_prices
            else:
                logging.debug("No 'Time Series (Daily)' in data")
                return []
        except Exception as e:
            logging.error(f"Error fetching stock data: {e}")
            return []

    def fetch_stock_prices(self, symbol):
        try:
            logging.debug(f"Beginning of fetch_stock_prices")
            stock_prices = self.database_operations_instance.fetch_stock_prices_from_db(
                symbol)
            if not stock_prices:
                self.fetch_and_insert_new_data(symbol)
                stock_prices = self.database_operations_instance.fetch_stock_prices_from_db(
                    symbol)
            logging.debug(f"Fetched stock prices")
            return stock_prices
        except Exception as e:
            logging.error(f"Error fetching stock prices: {e}")
            return []

    def fetch_and_insert_new_data(self, symbol):
        try:
            stock_prices = self.fetch_stock_data(symbol)
            self.database_operations_instance.insert_stock_prices(stock_prices)
            logging.debug(f"Fetched and inserted new stock data")
        except Exception as e:
            logging.error(f"Error fetching and inserting new stock data: {e}")
