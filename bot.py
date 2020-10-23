import discord
from discord.ext import commands
from settings import *
from database import *
from datascraping import *
import re

bot = discord.ext.commands.Bot('s!')


@bot.command()
async def join(ctx):
    """
    Adds user to the server game
    """
    add_user(ctx.author.id, ctx.guild.id)
    # checks if the user is already in the servers game
    if portfolio_exists(ctx.author.id, ctx.guild.id):
        await ctx.send("you're already in this servers stonks lulw")
    else:
        await ctx.send('you are now in stonks kekw')


@bot.command()
async def buy(ctx):
    """
    Performs a market buy of the quantity of the given stock
    """
    # gets author and server id's
    author = ctx.author.id
    server = ctx.guild.id

    # extract stock name out of message
    stock = ctx.message.content
    stock = re.sub('s!buy', '', stock)
    stock = re.sub('\d', '', stock)
    stock = stock[1:len(stock) - 1].upper()

    # extract quantity out of message
    quantity = ctx.message.content
    quantity = int(re.sub('\D', '', quantity))

    # get price of the stock
    stock_price = price(stock)
    cost = stock_price * quantity

    # checks if balance will go into negatives
    if (get_balance(author, server) - cost) < 0:
        await ctx.send("You don't have the funds for that!")
    else:
        # sets the balance to current balance minus cost
        set_balance(author, server, get_balance(author, server) - cost)
        # gives the user the quantity of stock
        set_stock(author, server, stock, int(get_stock(author, server, stock)) + quantity)

        await ctx.send("You bought **{0}** shares of **{1}**, at **${2}** per share.".format(quantity, stock,
                                                                                             stock_price))


@bot.command()
async def sell(ctx):
    """
    Performs a market sell of the quantity of the given stock
    """
    # get author and server id's
    author = ctx.author.id
    server = ctx.guild.id

    # extract stock name out of message
    stock = ctx.message.content
    stock = re.sub('s!sell', '', stock)
    stock = re.sub('\d', '', stock)
    stock = stock[1:len(stock) - 1].upper()

    # extract quantity out of message
    quantity = ctx.message.content
    quantity = int(re.sub('\D', '', quantity))

    # get price of the stock
    stock_price = price(stock)
    cost = stock_price * int(quantity)

    # checks if stock will go into negative
    if (get_stock(author, server, stock) - quantity) < 0:
        await ctx.send("You don't have that many shares of **{0}**.".format(stock))
    else:
        # subtracts quantity of stock from the users inventory
        set_stock(author, server, stock, int(get_stock(author, server, stock)) - quantity)
        # adds the cost of the stocks to the users inventory
        set_balance(author, server, get_balance(author, server) + cost)

        await ctx.send("You sold **{0}** shares of **{1}** at **${2}** per share.".format(quantity, stock, stock_price))

bot.run(BOT_TOKEN)
