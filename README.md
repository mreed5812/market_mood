# Project Title

Market Mood

## Description

Market Mood is an application designed to provide users with valuable insights into stock market trends and sentiment analysis. Users simply input a stock ticker, and the app fetches recent stock price history along with related news articles. Leveraging sentiment analysis algorithms, Market Mood gauges the sentiment expressed in these articles. Through a trend analysis, the application reveals correlations between stock price movements and sentiment shifts, empowering users with actionable intelligence for informed decision-making in the dynamic world of stock trading.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Database Schema](#database-schema)

## Installation

'''git clone https://github.com/mreed5812/market_mood.git'''

Navigate to the Repository Directory:
'''cd market_mood'''

Activate the virtual environment:
'''source venv/bin/activate'''

Install Depeendencies:
'''pip install -r requirements.txt'''


## Usage

To use market_mood, ensure virtual environment is running and then run the main program located within the 'src' folder:
'''python src/app.py'''

This will start the program locally at the following url: http://127.0.0.1:8080

Enter a stock ticker such as 'AAPL' or 'TSLA' into the search bar and click 'Search'.

The program will fetch recent stock price data along with any news articles related to that stock symbol and company. It will then display a time series for the stock price over recent months as well as the sentiment for any news related to the company/stock ticker.

## Database Schema

### `news_stories`

- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each news story.
- **source_name** (TEXT, NOT NULL): The name of the source from which the news story originated.
- **author** (TEXT): The author of the news story.
- **title** (TEXT, NOT NULL): The title of the news story.
- **description** (TEXT): A brief description of the news story.
- **url** (TEXT, NOT NULL): The URL link to the full news story.
- **url_to_image** (TEXT): The URL link to the image associated with the news story.
- **published_at** (TEXT, NOT NULL): The date and time when the news story was published.
- **content** (TEXT): The full content of the news story.
- **symbol** (TEXT, NOT NULL): The stock symbol related to the news story.
- **sentiment** (REAL): The sentiment score associated with the news story, indicating the sentiment (e.g., positive, negative, neutral).

### `stock_prices`

- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for each stock price entry.
- **symbol** (TEXT, NOT NULL): The stock symbol for which the price data is recorded.
- **date** (TEXT, NOT NULL): The date for which the stock price data is recorded.
- **open** (REAL, NOT NULL): The opening price of the stock on the given date.
- **high** (REAL, NOT NULL): The highest price of the stock on the given date.
- **low** (REAL, NOT NULL): The lowest price of the stock on the given date.
- **close** (REAL, NOT NULL): The closing price of the stock on the given date.
- **volume** (INTEGER, NOT NULL): The trading volume of the stock on the given date.

### SQL Schema Dump

```sql
CREATE TABLE news_stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    author TEXT,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    url_to_image TEXT,
    published_at TEXT NOT NULL,
    content TEXT,
    symbol TEXT NOT NULL,
    sentiment REAL
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL
);
