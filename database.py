import pymongo
from pymongo import MongoClient
from settings import *

cluster = MongoClient(DATABASE)
db = cluster[DB_NAME]
collection = db[COLLECTION_NAME]

post = {
    "_id": 0,
    "cash_balances": {
        "Server_0": default_balance,
        "Server_1": default_balance,
        "Server_2": default_balance,
    },
    "portfolios": {
        "Server_0": {
            "AAPL": 0,
            "MSFT": 0,
            "AMZN": 0,
            "GOOG": 0,
            "FB": 0,
            "TSLA": 0,
            "TSM": 0,
            "NVDA": 0,
            "PFE": 0,
            "T": 0,
            "ZM": 0,
            "AMD": 0,
            "BA": 0,
            "SQ": 0,
            "GE": 0,
            "ADSK": 0,
            "VRTX": 0,
            "PTON": 0,
            "NIO": 0,
            "F": 0,
            "CHWY": 0,
            "PLTR": 0,
            "NET": 0,
            "DKNG": 0,
            "FSLY": 0,
            "ARRY": 0,
            "HYLN": 0,
            "WKHS": 0,
        },
        "Server_1": {
            "AAPL": 0,
            "MSFT": 0,
            "AMZN": 0,
            "GOOG": 0,
            "FB": 0,
            "TSLA": 0,
            "TSM": 0,
            "NVDA": 0,
            "PFE": 0,
            "T": 0,
            "ZM": 0,
            "AMD": 0,
            "BA": 0,
            "SQ": 0,
            "GE": 0,
            "ADSK": 0,
            "VRTX": 0,
            "PTON": 0,
            "NIO": 0,
            "F": 0,
            "CHWY": 0,
            "PLTR": 0,
            "NET": 0,
            "DKNG": 0,
            "FSLY": 0,
            "ARRY": 0,
            "HYLN": 0,
            "WKHS": 0,
        },
        "Server_2": {
            "AAPL": 0,
            "MSFT": 0,
            "AMZN": 0,
            "GOOG": 0,
            "FB": 0,
            "TSLA": 0,
            "TSM": 0,
            "NVDA": 0,
            "PFE": 0,
            "T": 0,
            "ZM": 0,
            "AMD": 0,
            "BA": 0,
            "SQ": 0,
            "GE": 0,
            "ADSK": 0,
            "VRTX": 0,
            "PTON": 0,
            "NIO": 0,
            "F": 0,
            "CHWY": 0,
            "PLTR": 0,
            "NET": 0,
            "DKNG": 0,
            "FSLY": 0,
            "ARRY": 0,
            "HYLN": 0,
            "WKHS": 0,
        },
    },
}

#collection.insert_one(post)


def new_user(user_id):
    collection.insert_one({"_id": user_id})


def server_add_user(user_id, server_id):
    cash_balance = "cash_balances." + str(server_id)
    portfolio = "portfolio." + str(server_id)
    collection.update_one({"_id": user_id}, {"$set": {cash_balance: default_balance}})
    collection.update_one({"_id": user_id}, {"$set": {portfolio: {"AAPL": 0,
                                                       "MSFT": 0,
                                                       "AMZN": 0,
                                                       "GOOG": 0,
                                                       "FB": 0,
                                                       "TSLA": 0,
                                                       "TSM": 0,
                                                       "NVDA": 0,
                                                       "PFE": 0,
                                                       "T": 0,
                                                       "ZM": 0,
                                                       "AMD": 0,
                                                       "BA": 0,
                                                       "SQ": 0,
                                                       "GE": 0,
                                                       "ADSK": 0,
                                                       "VRTX": 0,
                                                       "PTON": 0,
                                                       "NIO": 0,
                                                       "F": 0,
                                                       "CHWY": 0,
                                                       "PLTR": 0,
                                                       "NET": 0,
                                                       "DKNG": 0,
                                                       "FSLY": 0,
                                                       "ARRY": 0,
                                                       "HYLN": 0,
                                                       "WKHS": 0, }}})


def set_stock(user_id, server_id, stock, quantity):
    updated_stock = "portfolio." + str(server_id) + "." + stock
    collection.update_one({"_id": user_id}, {"$set": {updated_stock: quantity} })


def get_stock(user_id, server_id, stock, quantity):


def set_balance(user_id, server_id, balance):

