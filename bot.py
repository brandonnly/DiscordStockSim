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
    """
    add_user(ctx.author.id, ctx.guild.id)
    # checks if the user is already in the servers game
    if portfolio_exists(ctx.author.id, ctx.guild.id):
        await ctx.send("you're already in this servers stonks lulw")
    else:
        await ctx.send('you are now in stonks kekw')


@bot.command()
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

    # get stock price and calculate total cost
    stock_price = get_price(stock_ticker)
    cost = stock_price * quantity

    # checks if balance will go into negatives
    if (get_balance(author, server) - cost) < 0:
        await ctx.send("You don't have the funds for that!")
    else:
        # sets the balance to current balance minus cost
        set_balance(author, server, get_balance(author, server) - cost)
        # gives the user the quantity of stock
        set_stock(author, server, stock_ticker, int(get_stock(author, server, stock_ticker)) + quantity)

        await ctx.send("You bought **{0}** shares of **{1}**, at **${2}** per share.".format(quantity, stock_ticker,
                                                                                             stock_price))
        await balance(ctx)


@bot.command()
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

    # get price of the stock
    stock_price = get_price(stock_ticker)
    cost = stock_price * quantity

    # checks if stock will go into negative
    if (get_stock(author, server, stock_ticker) - quantity) < 0:
        await ctx.send("You don't have that many shares of **{0}**.".format(stock_ticker))
    else:
        # subtracts quantity of stock from the users inventory
        set_stock(author, server, stock_ticker, int(get_stock(author, server, stock_ticker)) - quantity)
        # adds the cost of the stocks to the users inventory
        set_balance(author, server, get_balance(author, server) + cost)

        await ctx.send("You sold **{0}** shares of **{1}** at **${2}** per share.".format(quantity, stock_ticker,
                                                                                          stock_price))
        await balance(ctx)


@bot.command()
async def balance(ctx):
    """
    Returns your current balance
    """
    await ctx.send("**Current Balance:** ${0}".format(round(get_balance(ctx.author.id, ctx.guild.id), 2)))


@bot.command()
async def price(ctx, stock_ticker):
    """
    Returns the current share price of the given stock
    :param stock_ticker: the ticker symbol of the stock to check
    """
    stock_ticker = stock_ticker.upper()
    await ctx.send("Current **{0}** share value: **${1}**".format(stock_ticker, get_price(stock_ticker)))


@bot.command()
async def portfolio(ctx):
    """
    Returns an overview of your portfolio
    """
    users_portfolio = get_portfolio(ctx.author.id, ctx.guild.id)
    message = "**{0}'s** portfolio for **{1}**:\n```".format(ctx.author.name, ctx.guild.name)
    for stock_ticker in users_portfolio:
        message = message + "{0}: {1}\n".format(stock_ticker, users_portfolio[stock_ticker])
    message = message + "```"
    await ctx.send(message)


bot.run(BOT_TOKEN)
