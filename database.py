"""
Database functions for interacting with the backend
"""

from pymongo import MongoClient
from settings import *

cluster = MongoClient(DATABASE)
db = cluster[DB_NAME]
collection = db[COLLECTION_NAME]


def new_user(user_id):
    """
    Enters a brand new user into the database
    :param user_id: the users unique ID
    """
    collection.insert_one({"_id": user_id})
    print("Added new user with id", user_id)


def add_user(user_id, server_id):
    """
    Adds a user to the servers stonks game
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    """
    users = collection.find_one({"_id": user_id})
    if not user_exists(user_id):
        new_user(user_id)

    if not portfolio_exists(user_id, server_id):
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


def set_stock(user_id, server_id, stock, quantity):
    """
    Sets the a new value to the users stock count of that share
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :param stock: the stock ticker symbol
    :param quantity: the number to set to
    """
    updated_stock = "portfolio." + str(server_id) + "." + stock
    collection.update_one({"_id": user_id}, {"$set": {updated_stock: quantity}})
    print("Set the stock of", user_id, "in", server_id, "to", quantity, "for stock", stock)


def get_stock(user_id, server_id, stock):
    """
    Searches for and returns the users quantity of a given stock
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :param stock: the stock ticker symbol
    :return: the integer value of the users owned shared
    """
    portfolio = str(user_id) + ".portfolio." + str(server_id)
    user = collection.find_one({"_id": user_id})
    portfolio = user['portfolio']
    server = portfolio[str(server_id)]
    return server[stock]


def set_balance(user_id, server_id, balance):
    """
    Sets a new balance to the user in the servers stonks game
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :param balance: the new balance to set the account to
    """
    updated_balance = "cash_balances." + str(server_id)
    collection.update_one({"_id": user_id}, {"$set": {updated_balance: balance}})
    print("Set the balance of", user_id, "in", server_id, "to", balance)


def get_balance(user_id, server_id):
    """
    Returns the users balance in the stonks game
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :return: the floating value of the users balance
    """
    balance_to_find = str(user_id) + ".cash_balances." + str(server_id)
    user = collection.find_one({"_id": user_id})
    balance = user['cash_balances']
    return balance[str(server_id)]


def user_exists(user_id):
    """
    Checks if the user exists in the database
    :param user_id: the users unique ID
    :return: boolean value
    """
    users = collection.find_one({"_id": user_id})
    if users is None:
        return False
    else:
        return True


def portfolio_exists(user_id, server_id):
    """
    Checks if the user already has a portfolio in the server
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :return: boolean value
    """
    user = collection.find_one({"_id": user_id})
    portfolio = user['portfolio']
    try:
        server = portfolio[str(server_id)]
        return True
    except KeyError:
        return False


def get_portfolio(user_id, server_id):
    """
    Returns the users whole portfolio in the server as a dictionary
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :return: dictionary containing their portfolio
    """
    user = collection.find_one({"_id": user_id})
    portfolio = user['portfolio']
    return portfolio[str(server_id)]


print(get_portfolio(123, 234))
