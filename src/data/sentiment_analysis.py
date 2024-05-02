import sqlite3
from textblob import TextBlob

def update_sentiment_values():
    # Connect to the database
    conn = sqlite3.connect('market_mood.db')
    c = conn.cursor()
    
    # Retrieve news stories from the database
    c.execute('''SELECT * FROM news_stories''')
    rows = c.fetchall()
    
    # Iterate through each news story
    for row in rows:
        content = row[8]  # Assuming content is stored in the 8th column
        if content:
            # Calculate sentiment score using TextBlob
            blob = TextBlob(content)
            sentiment_score = blob.sentiment.polarity
            
            # Update the corresponding record in the database with the sentiment score
            c.execute('''UPDATE news_stories SET sentiment = ? WHERE id = ?''', (sentiment_score, row[0]))  # Assuming 'id' is the primary key
        
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


