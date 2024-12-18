"""Code by amiriiw"""

import os
import sys
import time
import json
import scrapy
import logging
import requests
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from typing import Any, List, Dict, Generator
from ThirdPartyFiles.FileManager import JsonFile
from scrapy.http.response.text import TextResponse
from scrapy.exceptions import NotConfigured, CloseSpider
from ThirdPartyFiles.TablesCenter import HandleSingleCoinTables


class HandleSpider(scrapy.Spider):
    """A Scrapy Spider to extract cryptocurrency information from CoinMarketCap."""

    name = "Z"
    
    def __init__(self, user_request: str, *args: Any, **kwargs: Any) -> None:
        """Initializes the spider with the cryptocurrency name and sets the start URL."""
        
        super().__init__(*args, **kwargs)
        self.user_request = user_request
        
    def start_requests(self) -> Generator[Request, None, None]:
        """Sends initial requests with custom headers via Splash for JavaScript handling."""
        
        try: 
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            urls = f"https://coinmarketcap.com/currencies/{self.user_request}/"
            
            yield SplashRequest(urls, headers=headers, callback=self.parse, args={"wait": 2})
        
        except Exception as e:
            self.logger.error(f"An error occurred while generating requests: {str(e)}", exc_info=True)
        
        
    def parse(self, response: TextResponse, **kwargs: Any) -> None:
        """Extracts cryptocurrency data from the page and external APIs, then saves it as JSON."""
        
        try:
            data = HandleSingleCoinTables.parse_single_coin(self.user_request, response)
            
            if not data: 
                
                self.logger.error(f"got an empty data", exc_info=True)
                return
            
            data = {
                "name": data["coin_name"],
                "logo": data["coin_logo"],
                "price": data["coin_price"],
                "24hour change": data["coin_24hour_change"],
                "lower price in 24 hour": data["coin_lower_price_in_24_hour"],
                "higher price in 24 hour": data["coin_higher_price_in_24_hour"],
                "all time-high": data["coin_all_time_high"],
                "all time-low": data["coin_all_time_low"],
                "about coin": data["about_coin"],
                "markets": data["markets"],
                "analytics": data["analytics"],
                "news": data["coin_news"],
            }
            
            JsonFile.save_to_json(data, self.user_request)
        
        except (NotConfigured, CloseSpider, requests.RequestException, json.JSONDecodeError) as e:
            self.logger.error(f"An error occurred while parse table: {str(e)}", exc_info=True)

        
if __name__ == "__main__":
    """Checks if the data is recent; if not, initiates the crawl."""
    
    try:
        if len(sys.argv) < 2:
            sys.exit(1)
    
        user_request = sys.argv[1]
        path = f"{user_request}.json"
        if os.path.isfile(path) and time.time() - os.path.getmtime(path) <= 30:
            sys.exit()
    
        crypto_info_spider = HandleSpider(user_request)
        process = CrawlerProcess()
        process.crawl(HandleSpider, user_request)
        process.start()

    except Exception as e:
        logging.error(f"An error occurred while start the spider: {str(e)}", exc_info=True)
