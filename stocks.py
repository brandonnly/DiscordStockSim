"""
All stock functions for getting information from the finnhub api
"""

import finnhub
from settings import *


finnhub_client = finnhub.Client(api_key=FINHUB_API_KEY)


def price(stock):
    numbers = finnhub_client.quote(stock)
    return numbers["c"]

