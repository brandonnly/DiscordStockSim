import discord
from discord.ext import commands
from settings import *


bot = discord.ext.commands.Bot('s!')


@bot.command()
async def hello(ctx):
    await ctx.send("hi!")

'''@bot.event():
async def on_member_join(member):

    print(f'(member) joined the server.')
async def on_member_remove(member):
    print(f'(member) has left a sever.')'''

bot.run(BOT_TOKEN)

