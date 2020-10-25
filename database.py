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
    # adds the user to the databse if they don't exist already
    if not user_exists(user_id):
        new_user(user_id)

    # adds the users balance to the server
    if not balance_exists(user_id, server_id):
        cash_balance = "cash_balances." + str(server_id)
        collection.update_one({"_id": user_id}, {"$set": {cash_balance: default_balance}})
        print("Added server", server_id, "portfolio to user", user_id)


def add_portfolio(user_id, server_id, stock, quantity):
    """
    Adds a portfolio to the user if they currently have no stocks.
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :param stock: stock ticker symbol
    :param quantity: quantity of stock to add
    """
    portfolio = "portfolio." + str(server_id)
    collection.update_one({"_id": user_id}, {"$set": {portfolio: {stock: quantity}}})


def delete_portfolio(user_id, server_id):
    """
    Removes the users portfolio
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    """
    portfolio = str(user_id) + ".portfolio." + str(server_id)
    collection.delete_one({portfolio})


def set_stock(user_id, server_id, stock, quantity):
    """
    Sets the a new value to the users stock count of that share
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :param stock: the stock ticker symbol
    :param quantity: the number to set to
    """
    updated_stock = "portfolio." + str(server_id) + "." + stock
    # removes the stock from the array if setting quantity to 0
    if quantity == 0:
        collection.update_one({"_id": user_id}, {"$unset": {updated_stock: quantity}})
    else:
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
    user = collection.find_one({"_id": user_id})
    try:
        portfolio = user['portfolio']
        server = portfolio[str(server_id)]
        return server[stock]
    # KeyError means that the user doesn't own any of the stock
    except KeyError:
        return 0


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


def balance_exists(user_id, server_id):
    """
    Checks if the user has a balance in the server
    :param user_id: the users unique ID
    :param server_id: the servers unique ID
    :return: boolean value
    """
    user = collection.find_one({"_id": user_id})
    try:
        balance = user['cash_balances']
        server = balance[str(server_id)]
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
