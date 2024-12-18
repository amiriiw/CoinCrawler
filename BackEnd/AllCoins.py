"""Code by amiriiw"""

import os
import sys
import time
import json
import scrapy
import logging
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http.response import Response
from typing import Any, List, Dict, Generator
from ThirdPartyFiles.FileManager import JsonFile
from ThirdPartyFiles.TablesCenter import HandleAllCoinsTables


class HandleSpider(scrapy.Spider):
    """Scrapy Spider for fetching cryptocurrency data from various sources based on the given position."""
    
    name = "Z"
    
    def __init__(self, user_request: str, *args: Any, **kwargs: Any) -> None:
        """Initializes the spider with the given crypto position."""

        super().__init__(*args, **kwargs)
        self.user_request = user_request

    def start_requests(self) -> Generator[Request, None, None]:
        """Sends requests to the start URLs with custom headers."""
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            urls = {
                "NewCrypto": "https://coinmarketcap.com/new/",
                "MostViewCrypto": "https://coinmarketcap.com/most-viewed-pages/",
                "TrendCrypto": "https://coinmarketcap.com/trending-cryptocurrencies/",
                "GainAndLose": "https://coinmarketcap.com/gainers-losers/",
                "CoinList": "https://coinmarketcap.com"
            }
            
            asked_url = urls.get(self.user_request)
            
            if not asked_url:
                self.logger.error(f"Invalid user request: {self.user_request}", exc_info=True)
                return
            
            yield scrapy.Request(asked_url, headers=headers, callback=self.parse)
        
        except Exception as e:
            self.logger.error(f"An error occurred while generating requests: {str(e)}", exc_info=True)
            
            
    def parse(self, response: Response, **kwargs: Any) -> None:
        """Selects the appropriate parser based on the crypto position."""
        
        try:
            parsers = {
                "NewCrypto": HandleAllCoinsTables.parse_new_crypto,
                "MostViewCrypto": HandleAllCoinsTables.parse_most_view_crypto,
                "TrendCrypto": HandleAllCoinsTables.parse_trend_crypto,
                "GainAndLose": HandleAllCoinsTables.parse_gain_and_lose,
                "CoinList": HandleAllCoinsTables.parse_coin_list
            }
            parser = parsers.get(self.user_request)
            
            if parser:
                data_list = parser()
                data_list = self.parse_table(response, data_list[0], data_list[1])
                
                if not data_list:
                    self.logger.error(f"Invalid data list: {data_list}")
                    return
                    
                JsonFile.save_to_json(data_list, user_request)
                
        except Exception as e:
            self.logger.error(f"An error occurred in parse function: {str(e)}", exc_info=True)

    def parse_table(self, response: Response, row_range: range, fields: List[str]) -> List[Dict[str, Any]]|None:
        """Parses table data from the page."""
        
        try: 
            data_list = []
            for i in row_range:
                row = response.css(f"table tr:nth-child({i})")
                
                if self.user_request == "gain_and_lose":
                    data = {field: row.css(f"td:nth-child({index + 2}) ::text").get() for index, field in enumerate(fields)}
                else:
                    data = {field: row.css(f"td:nth-child({index + 3}) ::text").get() for index, field in enumerate(fields)}
                data_list.append(data)
            
            return data_list
        
        except Exception as e: 
            self.logger.error(f"An error occurred while parse the table: {str(e)}", exc_info=True)
            
            
if __name__ == "__main__":
    """Checks if the file is recent; if not, starts the crawl."""
    
    positions = {
        "NewCrypto": "NewCrypto.json",
        "MostViewCrypto": "MostViewCrypto.json",
        "TrendCrypto": "TrendCrypto.json",
        "GainAndLose": "GainAndLose.json",
        "CoinList": "CoinList.json"
    }

    try:
        user_request = sys.argv[1]
        file_path = positions.get(user_request)
        
        if file_path and os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) <= 30:
            sys.exit()

        spider = HandleSpider(user_request) 
        process = CrawlerProcess()
 
        process.crawl(HandleSpider, user_request)
        process.start()
        
    except IndexError as i:
        logging.error(f"An error occurred while recive the argument: {str(i)}", exc_info=True)
    
    except Exception as e:
        logging.error(f"An error occurred while start the spider: {str(e)}", exc_info=True)