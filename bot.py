import discord
from discord.ext import commands
from settings import *


bot = discord.ext.commands.Bot('s!')


@bot.command()
async def hello(ctx):
    await ctx.send("hi!")


bot.run(BOT_TOKEN)
