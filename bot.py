"""
Main file for the bot and its commands
"""

import discord
from discord.ext import commands
from settings import *
from database import *
from stocks import *

bot = discord.ext.commands.Bot('s!')


@bot.command(aliases=['Join', 'enter', 'Enter', 'play', 'Play'], ignore_extra=True)
async def join(ctx):
    """
    Enters you into this servers stonks game
    """
    # checks if the user is already in the servers game
    try:
        if balance_exists(ctx.author.id, ctx.guild.id):
            await ctx.send(already_in_stonks)
        else:
            add_user(ctx.author.id, ctx.guild.id)
            await ctx.send(joined_stonks)
    # type error means that no object for the users balance exists
    except TypeError:
        add_user(ctx.author.id, ctx.guild.id)
        await ctx.send(joined_stonks)


@bot.command(aliases=['Buy', 'BUY'], ignore_extra=True)
async def buy(ctx, stock_ticker, quantity):
    """
    Performs a market buy of the quantity of the given stock
    :param stock_ticker: the ticker symbol of the stock
    :param quantity: the integer quantity to buy
    """
    # gets author and server id's
    author = ctx.author.id
    server = ctx.guild.id
    stock_ticker = stock_ticker.upper()
    quantity = int(quantity)

    # checks if the stock is a valid symbol - get_price returns 0 if not valid
    if get_price(stock_ticker) == 0:
        await ctx.send(invalid_stonk)
    else:
        # get stock price and calculate total cost
        stock_price = get_price(stock_ticker)
        cost = stock_price * quantity

        # checks if balance will go into negatives
        if (get_balance(author, server) - cost) < 0:
            await ctx.send(too_broke)
        else:
            # sets the balance to current balance minus cost
            set_balance(author, server, get_balance(author, server) - cost)
            # gives the user the quantity of stock
            try:
                set_stock(author, server, stock_ticker, int(get_stock(author, server, stock_ticker)) + quantity)
            # KeyError means that the user has never owned a stock so it adds one for them
            except KeyError:
                add_portfolio(author, server, stock_ticker, int(get_stock(author, server, stock_ticker)) + quantity)

            # lets the user know how much they bought at what price and their balance afterwards
            await ctx.send(bought_stonks.format(quantity, stock_ticker, stock_price))
            await balance(ctx)


@bot.command(aliases=['Sell', 'SELL'], ignore_extra=True)
async def sell(ctx, stock_ticker, quantity):
    """
    Performs a market sell of the quantity of the given stock
    :param stock_ticker: the ticker symbol of the stock
    :param quantity: the integer quantity to sell
    """
    # get author and server id's
    author = ctx.author.id
    server = ctx.guild.id
    stock_ticker = stock_ticker.upper()
    quantity = int(quantity)

    # checks if the stock is a valid symbol - get_price returns 0 if not valid
    if get_price(stock_ticker) == 0:
        await ctx.send(invalid_stonk)
    else:
        # get price of the stock and calculate total cost
        stock_price = get_price(stock_ticker)
        cost = stock_price * quantity

        # checks if stock will go into negative
        if (get_stock(author, server, stock_ticker) - quantity) < 0:
            await ctx.send(not_enough_stonks.format(stock_ticker))
        else:
            # subtracts quantity of stock from the users inventory
            set_stock(author, server, stock_ticker, int(get_stock(author, server, stock_ticker)) - quantity)
            # adds the cost of the stocks to the users inventory
            set_balance(author, server, get_balance(author, server) + cost)

            # lets the user know how much they bought at what price and their balance afterwards
            await ctx.send(sold_stonks.format(quantity, stock_ticker, stock_price))
            await balance(ctx)


@bot.command(aliases=['Balance', 'bal', 'Bal'], ignore_extra=True)
async def balance(ctx):
    """
    Returns your current balance
    """
    await ctx.send("**Current Balance:** ${0}".format(round(get_balance(ctx.author.id, ctx.guild.id), 2)))


@bot.command(ignore_extra=True)
async def price(ctx, stock_ticker):
    """
    Returns the current share price of the given stock
    :param stock_ticker: the ticker symbol of the stock to check
    """
    stock_ticker = stock_ticker.upper()
    if get_price(stock_ticker) == 0:
        await ctx.send(invalid_stonk)
    else:
        await ctx.send(current_stonk_value.format(stock_ticker, get_price(stock_ticker)))


@bot.command(aliases=['stocks', 'stock'], ignore_extra=True)
async def stonks(ctx):
    """
    Returns an overview of all your owned stonks
    """
    try:
        users_portfolio = get_portfolio(ctx.author.id, ctx.guild.id)
        # message template
        message = "**{0}'s** stonks for **{1}**:\n```".format(ctx.author.name, ctx.guild.name)
        # loops through the users portfolio and adds them to the message
        for stock_ticker in users_portfolio:
            quantity = users_portfolio[stock_ticker]
            message = message + "{0}: {1} - valued at ${2}\n".format(stock_ticker, quantity, (get_price(stock_ticker) *
                                                                                              quantity))
        message = message + "```"

        # check if the message has no stocks and is just the template
        if len(message) == 80:
            await ctx.send(no_stonks)
        else:
            await ctx.send(message)

    # KeyError means that the portfolio doesn't exist at all
    except KeyError:
        await ctx.send(no_stonks)


@bot.command(ignore_extra=True)
async def portfolio(ctx):
    """
    Returns the users portfolio
    """

    author_id = ctx.author.id
    author_name = ctx.author.name
    server_id = ctx.guild.id
    server_name = ctx.guild.name

    # gets the users portfolio
    users_portfolio = get_portfolio(author_id, server_id)

    # portfolio variables
    value = 0
    quantity = 0
    stocks = 0
    cash_balance = round(get_balance(author_id, server_id), 2)

    # loop through users portfolio and add to counters
    for stock_ticker in users_portfolio:
        stock_quantity = users_portfolio[stock_ticker]

        value += get_price(stock_ticker) * stock_quantity
        quantity += stock_quantity
        stocks += 1

    # sends the users portfolio
    message = "**{0}'s** portfolio for **{1}**:\n```py\n".format(author_name, server_name)
    message = message + "Portfolio Value = ${0} \n\nCash Balance = ${1} \nStonks Value = ${2}".format(cash_balance +
                                                                                                      value,
                                                                                                      cash_balance,
                                                                                                      value)
    message = message + "\n\nUnique Stonks Owned = {0} \nTotal Stonks Owned = {1}".format(stocks, quantity)
    message = message + "```"
    message = message + "\nTo view your individual stonks and their values use **s!stonks**"
    await ctx.send(message)


bot.run(BOT_TOKEN)
