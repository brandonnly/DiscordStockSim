"""
All stock functions for getting information from the finnhub api
"""

import finnhub
from settings import *


finnhub_client = finnhub.Client(api_key=FINHUB_API_KEY)


def get_price(stock_ticker):
    """
    Returns the current trading price of stock
    :param stock_ticker: stock ticker symbol to check
    :return: the price of a single share
    """
    stock_info = finnhub_client.quote(stock_ticker)
    return stock_info['c']
