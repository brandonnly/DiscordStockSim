"""
All stock functions for getting information from the finnhub api
"""

import finnhub
from settings import *


finnhub_client = finnhub.Client(api_key=FINHUB_API_KEY)


def get_price(stock_ticker):
    stock_info = finnhub_client.quote(stock_ticker)
    return stock_info['c']
