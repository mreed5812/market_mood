import requests
import sqlite3
import os
from datetime import datetime, timedelta
from . import database_operations

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'market_mood.db')

def fetch_stock_data(symbol):
    API_KEY = 'SFRHBUTCXB3RDG5S'
    one_month_ago = datetime.now() - timedelta(days=30*1)
    start_date = one_month_ago.strftime('%Y-%m-%d')
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact&datatype=json&startdate={start_date}'
    print(url)
    response = requests.get(url)
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
        return stock_prices
    else:
        return []

def fetch_stock_prices(symbol):
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        c = conn.cursor()

        thirty_days_ago = datetime.now() - timedelta(days=30)
        start_date = thirty_days_ago.strftime('%Y-%m-%d')

        c.execute('''SELECT * FROM stock_prices 
                     WHERE symbol = ? AND date >= ? 
                     ORDER BY date DESC''', (symbol, start_date))
        rows = c.fetchall()

        conn.close()

        if rows:
            return format_stock_data(rows)
        else:
            fetch_and_insert_new_data(symbol)
            return fetch_stock_prices_from_db(symbol)
    except Exception as e:
        print(f"Error fetching stock prices from database: {e}")
        return []

def format_stock_data(rows):
    stock_prices = []
    for row in rows:
        stock_prices.append({
            'symbol': row[1],
            'date': row[2],
            'open': row[3],
            'high': row[4],
            'low': row[5],
            'close': row[6],
            'volume': row[7]
        })
    return stock_prices

def fetch_and_insert_new_data(symbol):
    stock_prices = fetch_stock_data(symbol)
    if stock_prices:
        database_operations.insert_stock_prices(stock_prices)
    else:
        print("Error fetching stock data from API.")

def fetch_stock_prices_from_db(symbol):
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()

    thirty_days_ago = datetime.now() - timedelta(days=30)
    start_date = thirty_days_ago.strftime('%Y-%m-%d')

    c.execute('''SELECT * FROM stock_prices 
                 WHERE symbol = ? AND date >= ? 
                 ORDER BY date DESC''', (symbol, start_date))
    rows = c.fetchall()

    conn.close()

    return format_stock_data(rows)
