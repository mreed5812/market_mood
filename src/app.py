import logging
from flask import Flask, request, render_template
from data_collector.StockDataFetcher import StockDataFetcher
from data_collector.NewsDataFetcher import NewsDataFetcher
from data_analyzer.SentimentAnalyzer import SentimentAnalyzer
from datetime import datetime
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

stock_data_fetcher = StockDataFetcher()
news_data_fetcher = NewsDataFetcher()
sentiment_analyzer = SentimentAnalyzer()


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
    logging.debug(f"Received search query: {search_query}")
    if search_query:
        # Fetch stock prices
        try:
            stock_prices = stock_data_fetcher.fetch_stock_prices(search_query)
            logging.debug(f"Fetched stock prices")
        except Exception as e:
            logging.error(f"Error fetching stock prices: {e}")
            return f"Error fetching stock prices: {e}", 500

        try:
            news_stories = news_data_fetcher.fetch_news(search_query)
            # logging.debug(f"Fetched news stories: {news_stories}")
        except Exception as e:
            logging.error(f"Error fetching news stories: {e}")
            return f"Error fetching news stories: {e}", 500

        # Update sentiment values
        try:
            sentiment_analyzer.update_sentiment_values(search_query)
            logging.debug(f"Updated sentiment values for: {search_query}")
        except Exception as e:
            logging.error(f"Error updating sentiment values: {e}")
            return f"Error updating sentiment values: {e}", 500

        time.sleep(5)

        # I know there's a better way to do this but for now I'm stupidly re-fetching news data after sentiment has been added
        try:
            news_stories = news_data_fetcher.fetch_news(search_query)
            # logging.debug(f"Fetched news stories after sentiment update: {news_stories}")
        except Exception as e:
            logging.error(
                f"Error fetching news stories after sentiment update: {e}")
            return f"Error fetching news stories after sentiment update: {e}", 500

        if stock_prices and news_stories:
            # Sort stock prices by date
            try:
                stock_prices.sort(
                    key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
                logging.debug(f"Sorted stock prices")
            except Exception as e:
                logging.error(f"Error sorting stock prices: {e}")
                return f"Error sorting stock prices: {e}", 500

            # Extract date and close price for plotting
            try:
                dates = [datetime.strptime(price['date'], '%Y-%m-%d')
                         for price in stock_prices]
                close_prices = [price['close'] for price in stock_prices]
                logging.debug(f"Extracted dates and close prices")
            except Exception as e:
                logging.error(f"Error extracting dates and close prices: {e}")
                return f"Error extracting dates and close prices: {e}", 500

            # Extract sentiment values for plotting
            try:
                sentiment_values = [story.get('sentiment', 0)
                                    for story in news_stories]
                logging.debug(f"Extracted sentiment values")
            except Exception as e:
                logging.error(f"Error extracting sentiment values: {e}")
                return f"Error extracting sentiment values: {e}", 500

            # Render a time series chart using Plotly
            return render_template("time_series_chart.html", dates=dates, close_prices=close_prices, symbol=search_query, sentiment_values=sentiment_values)

    return "Invalid search query", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
