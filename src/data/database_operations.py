import os
import sqlite3

def insert_stock_prices(stock_prices):
    db_path = os.path.join(os.getcwd(), 'market_mood.db')
    conn = sqlite3.connect(db_path)
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

def insert_news_stories(news_stories):
    conn = sqlite3.connect('market_mood.db')
    c = conn.cursor()
    for story in news_stories:
        # Check if the record already exists in the database
        c.execute('''SELECT COUNT(*) FROM news_stories 
                     WHERE source_name = ? AND published_at = ?''', (story.get('source', {}).get('name', ''), story.get('publishedAt', '')))
        existing_records = c.fetchone()[0]
        if existing_records == 0:  # If no existing record found, insert the new record
            c.execute('''INSERT INTO news_stories (source_name, author, title, description, url, url_to_image, published_at, content)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (story.get('source', {}).get('name', ''), story.get('author', ''),
                                                               story.get('title', ''), story.get('description', ''),
                                                               story.get('url', ''), story.get('urlToImage', ''),
                                                               story.get('publishedAt', ''), story.get('content', '')))
    conn.commit()
    conn.close()
