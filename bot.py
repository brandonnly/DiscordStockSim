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
    if portfolio_exists(ctx.author.id, ctx.guild.id):
        await ctx.send("you're already in this servers stonks lulw")
    else:
        await ctx.send('you are now in stonks kekw')


@bot.command()
async def buy(ctx):
    """
    Performs a market buy of the quantity of the given stock
    """
    author = ctx.author.id
    server = ctx.guild.id
    length = len(ctx.message.content)
    # extract stock name out of message
    stock = ctx.message.content
    stock = re.sub('s!buy', '', stock)
    stock = re.sub('\d', '', stock)
    stock = stock[1:len(stock) - 1]

    # extract quantity out of message
    quantity = ctx.message.content
    quantity = re.sub('\D', '', quantity)

    # get price of the stock
    stock_price = price(stock)
    cost = stock_price * int(quantity)

    # checks if balance will go into negatives
    if (get_balance(author, server) - cost) < 0:
        await ctx.send("You don't have the funds for that!")

    else:
        # sets the balance to current balance minus cost
        set_balance(author, server, get_balance(author, server) - cost)

        # gives the user the quantity of stock
        set_stock(author, server, stock, int(get_stock(author, server, stock)) + int(quantity))

        await ctx.send("You bought **{0}** shares of **{1}**, at **${2}** per share.".format(quantity, stock, stock_price))


bot.run(BOT_TOKEN)
