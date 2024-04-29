
#!/usr/bin/env python3

from flask import Flask, request, render_template
from data import stock_data, news_data, database_operations

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    <h1>Market Mood</h1>
    <p>A tool for helping investors based on market sentiment and historic stock pricing.</p>
    <form action="/search" method="POST">
        <input name="search_query" placeholder="Enter stock symbol or company name">
        <input type="submit" value="Search">
    </form>
    '''

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_query", "")
    if search_query:
        # Fetch stock prices and news data
        stock_prices = stock_data.fetch_stock_prices_from_db(search_query)
        news_stories = news_data.fetch_news(search_query)
        
        if stock_prices is not None:
            # Insert stock prices into the database
            database_operations.insert_stock_prices(stock_prices)
        
        if news_stories is not None:
            # Insert news stories into the database
            database_operations.insert_news_stories(news_stories)
        
        # Process the retrieved data and render a template to display it
        return render_template("search_results.html", stock_prices=stock_prices, news_stories=news_stories)

    else:
        return "Please enter a search query."

if __name__ == "__main__":
    # Run the Flask application on port 8080
    app.run(host="0.0.0.0", port=8080)
