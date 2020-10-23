from pymongo import MongoClient
from pymongo.errors import *

from settings import *

cluster = MongoClient(DATABASE)
db = cluster[DB_NAME]
collection = db[COLLECTION_NAME]


def new_user(user_id):
    collection.insert_one({"_id": user_id})
    print("Added new user with id", user_id)


def add_user(user_id, server_id):
    users = collection.find({"_id": user_id})
    try:
        new_user(user_id)
    except DuplicateKeyError:
        pass

    try:
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
        print("Added server", server_id, "portfolio to user", user_id)
    except DuplicateKeyError:
        pass


def set_stock(user_id, server_id, stock, quantity):
    updated_stock = "portfolio." + str(server_id) + "." + stock
    collection.update_one({"_id": user_id}, {"$set": {updated_stock: quantity}})
    print("Set the stock of", user_id, "in", server_id, "to", quantity, "for stock", stock)


def get_stock(user_id, server_id, stock):
    portfolio = str(user_id) + ".portfolio." + str(server_id)
    user = collection.find_one({"_id": user_id})
    portfolio = user['portfolio']
    server = portfolio[str(server_id)]
    return server[stock]


def set_balance(user_id, server_id, balance):
    updated_balance = "cash_balances." + str(server_id)
    collection.update_one({"_id": user_id}, {"$set": {updated_balance: balance}})
    print("Set the balance of", user_id, "in", server_id, "to", balance)


def get_balance(user_id, server_id):
    balance_to_find = str(user_id) + ".cash_balances." + str(server_id)
    user = collection.find_one({"_id": user_id})
    balance = user['cash_balances']
    return balance[str(server_id)]

