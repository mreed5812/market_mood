import os
import sqlite3

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'market_mood.db')


def insert_stock_prices(stock_prices):
    #db_path = os.path.join(os.getcwd(), 'market_mood.db')
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()
    for price in stock_prices:
        # Check if the record already exists in the database
        c.execute('''SELECT COUNT(*) FROM stock_prices 
                     WHERE symbol = ? AND date = ?''', (price['symbol'], price['date']))
        existing_records = c.fetchone()[0]
        if existing_records == 0:  # If no existing record found, insert the new record
            c.execute('''INSERT INTO stock_prices (symbol, date, open, high, low, close, volume)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', (price['symbol'], price['date'], price['open'],
                                                           price['high'], price['low'], price['close'],
                                                           price['volume']))
    conn.commit()
    conn.close()

def insert_news_stories(news_stories, symbol):
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()
    for story in news_stories:
        # Check if the record already exists in the database
        c.execute('''SELECT COUNT(*) FROM news_stories 
                     WHERE source_name = ? AND published_at = ?''', (story.get('source', {}).get('name', ''), story.get('publishedAt', '')))
        existing_records = c.fetchone()[0]
        if existing_records == 0:  # If no existing record found, insert the new record
            c.execute('''INSERT INTO news_stories (source_name, author, title, description, url, url_to_image, published_at, content, symbol)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (story.get('source', {}).get('name', ''), story.get('author', ''),
                                                               story.get('title', ''), story.get('description', ''),
                                                               story.get('url', ''), story.get('urlToImage', ''),
                                                               story.get('publishedAt', ''), story.get('content', ''), symbol))
    conn.commit()
    conn.close()


def fetch_news_stories_by_symbol_and_date_range(symbol, start_date, end_date):
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()
    c.execute('''SELECT * FROM news_stories WHERE symbol = ? AND published_at BETWEEN ? AND ?''', (symbol, start_date, end_date))
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
