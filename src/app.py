from flask import Flask, request, render_template
from data_collector import stock_data, news_data, database_operations
from data_analyzer import sentiment_analysis
from datetime import datetime
import time

app = Flask(__name__)


@app.route("/")
def main():
    return '''
    <h1>Market Mood</h1>
    <p>A tool for helping investors based on market sentiment and historic stock pricing.</p>
    <form action="/search" method="POST">
        <input name="search_query" placeholder="Enter stock symbol">
        <input type="submit" value="Search">
    </form>
    '''

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_query", "")
    if search_query:
        # Fetch stock prices
        stock_prices = stock_data.fetch_stock_prices_from_db(search_query)
        news_stories = news_data.fetch_news(search_query)
        
        # Update sentiment values
        sentiment_analysis.update_sentiment_values(search_query)
        time.sleep(5)
        
        # Fetch news stories from the database after updating sentiment values
        news_stories = news_data.fetch_news(search_query)
        
        if stock_prices and news_stories:
            # Sort stock prices by date
            stock_prices.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

            # Extract date and close price for plotting
            dates = [datetime.strptime(price['date'], '%Y-%m-%d') for price in stock_prices]
            close_prices = [price['close'] for price in stock_prices]

            # Extract sentiment values for plotting
            sentiment_values = [story.get('sentiment', 0) for story in news_stories]  # Use get() to handle missing 'sentiment' key
            
            # Render a time series chart using Plotly
            return render_template("time_series_chart.html", dates=dates, close_prices=close_prices, symbol=search_query, sentiment_values=sentiment_values)
        else:
            return "No stock prices available for the specified symbol."
    else:
        return "Please enter a search query."



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
