# CoinCrawler

CoinCrawler is a Python-based web application designed to crawl and display cryptocurrency data. It provides users with insights such as trending coins, gainers/losers, and detailed information about specific cryptocurrencies using Flask and Scrapy frameworks.

## Features

- **Cryptocurrency Data Crawling:** Fetch data from CoinMarketCap for various categories like new cryptos, most viewed, trending, and gainers/losers.
- **Single Coin Lookup:** Retrieve detailed information about a specific cryptocurrency, including price, 24-hour change, and market analytics.
- **JSON Data Handling:** Save crawled data to JSON files for further processing.
- **Dynamic Web Application:** User-friendly interface to fetch and display data using Flask.
- **Real-Time Updates:** Ensures data freshness by checking file modification times.

## File Structure

```
CoinCrawler/
|
|-- app.py                    # Main Flask application
|-- templates/                # HTML templates for the web interface
|
|-- BackEnd/
|   |-- AllCoins.py           # Handles scraping for all coins categories
|   |-- SingleCoin.py         # Handles scraping for a specific coin
|   |-- ThirdPartyFiles/
|       |-- FileManager.py    # Utility for JSON file operations
|       |-- TablesCenter.py   # Parsers for extracting data
|
|-- requirements.txt          # Python dependencies
|-- README.md                 # Project README file
|-- LICENSE                   # LICENSE
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amiriiw/CoinCrawler.git
   cd CoinCrawler
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python3 app.py
   ```
5. Access the web interface at [http://localhost:5000](http://localhost:5000).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
