import requests
from datetime import datetime, timedelta

def fetch_stock_prices(symbol):
    API_KEY = 'SFRHBUTCXB3RDG5S'
    
    # Calculate the start date as 6 months ago from the current date
    six_months_ago = datetime.now() - timedelta(days=30*6)
    start_date = six_months_ago.strftime('%Y-%m-%d')

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact&datatype=json&startdate={start_date}'
    
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' in data:
        # Extracting stock prices from the response
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
        return stock_prices
    else:
        return None
