# Project Title

Market Mood

## Description

Market Mood is an application designed to provide users with valuable insights into stock market trends and sentiment analysis. Users simply input a stock ticker, and the app fetches recent stock price history along with related news articles. Leveraging sentiment analysis algorithms, Market Mood gauges the sentiment expressed in these articles. Through a trend analysis, the application reveals correlations between stock price movements and sentiment shifts, empowering users with actionable intelligence for informed decision-making in the dynamic world of stock trading.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)

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

