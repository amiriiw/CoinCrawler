"""Code by amiriiw"""

import logging
import requests
from typing import List, Dict, Text
from scrapy.http.response.text import TextResponse


class HandleAllCoinsTables:
    
    @staticmethod
    def parse_new_crypto() -> List:
        """Extracts data from the 'new crypto' page."""
        
        fields = ["name", "price", "1hour change", "24hour change", "fully diluted", "volume"]
        return [range(1, 32), fields]

    @staticmethod
    def parse_most_view_crypto() -> List:
        """Extracts data from the 'most viewed crypto' page."""
        
        fields = ["name", "price", "24hour change", "1week change", "1month change", "marketcap"]
        return [range(1, 32), fields]

    @staticmethod
    def parse_trend_crypto() -> List:
        """Extracts data from the 'trending crypto' page."""
        
        fields = ["name", "price", "24hour change", "1week change", "30day", "marketcap", "volume"]
        return [range(1, 32), fields]

    @staticmethod
    def parse_gain_and_lose() -> List:
        """Extracts data from the 'gainers and losers' page."""
        
        fields = ["name", "price", "24hour change", "volume"]
        return [range(1, 48), fields]

    @staticmethod
    def parse_coin_list() -> List:
        """Extracts data from the 'coin list' page."""
        
        fields = ["name", "price", "1hour change", "24hour change", "1month change", "gain_lose_num", "volume"]
        return [range(1, 32), fields]


class HandleSingleCoinTables:
    
    @staticmethod
    def parse_single_coin(coin_name: str, response: TextResponse) -> Dict|None:
        f"""Extracts data from the '{coin_name}' page."""
        
        try:
            coin_markets_response = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={coin_name}&start=1&limit=10&category=spot&centerType=cex&sort=cmc_rank_advanced&direction=desc&spotUntracked=true")
            coin_markets = coin_markets_response.json().get("data", {}).get("marketPairs", [])
            coin_markets_data = [
                {
                    "rank": market.get("rank"),
                    "exchangeId": market.get("exchangeId"),
                    "exchangeName": market.get("exchangeName"),
                    "marketPair": market.get("marketPair"),
                    "marketUrl": market.get("marketUrl"),
                    "baseSymbol": market.get("baseSymbol"),
                    "price": market.get("price"),
                    "volumeUsd": market.get("volumeUsd"),
                    "volumeBase": market.get("volumeBase"),
                    "volumeQuote": market.get("volumeQuote"),
                    "volumePercent": market.get("volumePercent"),
                    "type": market.get("type"),
                    "quotes": market.get("quotes")
                }
                for market in coin_markets
            ]
    
            crypto_id = response.css("div.sc-f70bb44c-0.iQEJet.BaseChip_labelWrapper__lZ4ii ::text").get()
            coin_analytics_data_response = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/info/get-analytics?cryptoId={crypto_id}&timeRangeType=month1")
            coin_analytics_data = coin_analytics_data_response.json()
    
            tables = {
                "coin_lower_price_in_24_hour": response.css("#__next div:nth-child(2) section:nth-child(2) > div > div:nth-child(4) div:nth-child(2) div:nth-child(1) span ::text").get(),
                "coin_higher_price_in_24_hour": response.css("#__next section:nth-child(2) div:nth-child(4) div:nth-child(2) div:nth-child(2) span ::text").get(),
                "coin_all_time_high": response.css("#__next section:nth-child(2) div:nth-child(4) div:nth-child(3) div:nth-child(2) span ::text").get(),
                "coin_all_time_low": response.css("#__next section:nth-child(2) div:nth-child(4) div:nth-child(4) div:nth-child(2) span ::text").get(),
                "about_coin": "".join(response.css("#section-coin-about section div:nth-child(1) div:nth-child(2) div div ::text").getall()).strip(),
                "coin_name": response.css("#section-coin-overview div:nth-child(1) h1:nth-child(2) span ::text").get(),
                "coin_24hour_change": response.css("#section-coin-overview div:nth-child(2) div div p ::text").get(),
                "coin_logo": response.css("#section-coin-overview div:nth-child(1) div img ::attr(src)").get(),
                "coin_price": response.css("#section-coin-overview > div:nth-child(2) span ::text").get(),
                "coin_news": requests.post("https://api.coinmarketcap.com/aggr/v4/content/user").json(),
                "analytics": coin_analytics_data,
                "markets": coin_markets_data,
            }
            
            return tables
        
        except Exception as e:
            logging.error(f"An error occurred while send tables info from third party files -> TablesCenter: {str(e)}", exc_info=True)
        