import discord
from discord.ext import commands
from settings import *
from database import *
from datascraping import *



bot = discord.ext.commands.Bot('s!')

@bot.command()
async def join(ctx):
    user_id = ctx.author.id
    server_id = ctx.author.id
    new_user(ctx.author.id)
    add_user(ctx.author.id, ctx.guild.id)
    await ctx.send('you are now in stonks kekw')

bot.run(BOT_TOKEN)

