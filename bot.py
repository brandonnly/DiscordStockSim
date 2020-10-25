"""
Main file for the bot and its commands
"""

import discord
from discord.ext import commands
from settings import *
from database import *
from stocks import *

bot = discord.ext.commands.Bot('s!')


@bot.command()
async def join(ctx):
    """
    Enters you into this servers stonks game
    :param ctx: pass context
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


@bot.command()
async def buy(ctx, stock_ticker, quantity):
    """
    Performs a market buy of the quantity of the given stock
    :param ctx: pass context
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


@bot.command()
async def sell(ctx, stock_ticker, quantity):
    """
    Performs a market sell of the quantity of the given stock
    :param ctx: pass context
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


@bot.command()
async def balance(ctx):
    """
    Returns your current balance
    :param ctx: pass context
    """
    await ctx.send("**Current Balance:** ${0}".format(round(get_balance(ctx.author.id, ctx.guild.id), 2)))


@bot.command()
async def price(ctx, stock_ticker):
    """
    Returns the current share price of the given stock
    :param ctx: pass context
    :param stock_ticker: the ticker symbol of the stock to check
    """
    stock_ticker = stock_ticker.upper()
    if get_price(stock_ticker) == 0:
        await ctx.send(invalid_stonk)
    else:
        await ctx.send(current_stonk_value.format(stock_ticker, get_price(stock_ticker)))


@bot.command()
async def stonks(ctx):
    """
    Returns an overview of all your owned stonks
    :param ctx: pass context
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


bot.run(BOT_TOKEN)
