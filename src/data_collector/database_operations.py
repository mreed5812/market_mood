import os
import sqlite3
from datetime import datetime, timedelta


class DatabaseOperations:
    def __init__(self):
        self.DB_FILE_PATH = os.path.join(os.path.dirname(
            __file__), '..', '..', 'database', 'market_mood.db')

    def insert_stock_prices(self, stock_prices):
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()
        for price in stock_prices:
            c.execute('''SELECT COUNT(*) FROM stock_prices WHERE symbol = ? AND date = ?''',
                      (price['symbol'], price['date']))
            existing_records = c.fetchone()[0]
            if existing_records == 0:
                c.execute('''INSERT INTO stock_prices (symbol, date, open, high, low, close, volume)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''', (price['symbol'], price['date'], price['open'], price['high'],
                                                               price['low'], price['close'], price['volume']))
        conn.commit()
        conn.close()

    def insert_news_stories(self, news_stories, symbol):
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()
        for story in news_stories:
            source_name = story.get('source', {}).get('name', '')
            published_at = story.get('publishedAt', '')

            c.execute('''SELECT COUNT(*) FROM news_stories WHERE source_name = ? AND published_at = ?''',
                      (source_name, published_at))
            existing_records = c.fetchone()[0]
            if existing_records == 0:
                c.execute('''INSERT INTO news_stories (source_name, author, title, description, url, url_to_image, published_at, content, symbol)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    source_name,
                    story.get('author', ''),
                    story.get('title', ''),
                    story.get('description', ''),
                    story.get('url', ''),
                    story.get('urlToImage', ''),
                    published_at,
                    story.get('content', ''),
                    symbol
                ))
        conn.commit()
        conn.close()

    def fetch_news_stories_by_symbol_and_date_range(self, symbol, start_date, end_date):
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()
        c.execute('''SELECT * FROM news_stories WHERE symbol = ? AND published_at BETWEEN ? AND ?''',
                  (symbol, start_date, end_date))
        news_stories = []
        for row in c.fetchall():
            news_story = {
                'source_name': row[1],
                'author': row[2],
                'title': row[3],
                'description': row[4],
                'url': row[5],
                'url_to_image': row[6],
                'published_at': row[7],
                'content': row[8],
                'symbol': row[9],
                'sentiment': row[10]
            }
            news_stories.append(news_story)
        conn.close()
        return news_stories

    def fetch_stock_prices_from_db(self, symbol):
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()

        thirty_days_ago = datetime.now() - timedelta(days=30)
        start_date = thirty_days_ago.strftime('%Y-%m-%d')

        c.execute('''SELECT * FROM stock_prices 
                     WHERE symbol = ? AND date >= ? 
                     ORDER BY date DESC''', (symbol, start_date))
        rows = c.fetchall()

        conn.close()

        if rows:
            return self.format_stock_data(rows)
        else:
            return []

    def format_stock_data(self, rows):
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
