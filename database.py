import pymongo
from pymongo import MongoClient
from settings import *


cluster = MongoClient(DATABASE)
db = cluster[DB_NAME]
collection = db[COLLECTION_NAME]

post = {
    "_id": 0,
    "cash_balances": {
        "Server_0": 10000,
        "Server_1": 10000,
        "Server_2": 10000,
    },
    "portfolios": {
        "AAPL": 0,
        "GOOG": 0,
        "AMZN": 0,
    },
}

collection.insert_one(post)