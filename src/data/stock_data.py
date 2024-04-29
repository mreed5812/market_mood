import requests
import sqlite3
from datetime import datetime, timedelta

def fetch_stock_prices(symbol):
    API_KEY = 'SFRHBUTCXB3RDG5S'
    
    # Calculate the start date as 6 months ago from the current date
    one_month_ago = datetime.now() - timedelta(days=30*1)
    start_date = one_month_ago.strftime('%Y-%m-%d')

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact&datatype=json&startdate={start_date}'
    print(url)
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
        return []  # Return an empty list if no data is available

def fetch_stock_prices_from_db(symbol):
    # Connect to the database
    conn = sqlite3.connect('market_mood.db')
    c = conn.cursor()

    # Calculate the start date as 6 months ago from the current date
    one_month_ago = datetime.now() - timedelta(days=30*1)
    start_date = one_month_ago.strftime('%Y-%m-%d')

    # Query the database for stock prices
    c.execute('''SELECT * FROM stock_prices 
                 WHERE symbol = ? AND date >= ? 
                 ORDER BY date DESC''', (symbol, start_date))
    rows = c.fetchall()

    # Close the database connection
    conn.close()

    # Convert the fetched rows into a list of dictionaries
    stock_prices = []
    for row in rows:
        stock_prices.append({
            'symbol': row[0],
            'date': row[1],
            'open': row[2],
            'high': row[3],
            'low': row[4],
            'close': row[5],
            'volume': row[6]
        })

    return stock_prices
