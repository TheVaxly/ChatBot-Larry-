import responses
import random
from discord.ext import commands
import discord
import praw
import ask
import clear_all
import clear_user
import clear_bot
import roll
import reddit

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

dice_history = []
symbol = "```"

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command(name='ask')
async def ask_command(ctx, *, user_input):
    await ask.ask_command(ctx, user_input=user_input)

@client.command(name='roll')
async def roll_command(ctx, *, dice: str = ''):
    await roll.roll_command(ctx, dice=dice)

@client.command(name='clearbot')
async def clear_command(ctx, amount: int):
    await clear_bot.clear_command(ctx, amount)

@client.command(name='clearuser')
async def clearuser_command(ctx, user: discord.Member = None, amount: int = None):
    await clear_user.clearuser_command(ctx, user, amount)

@client.command(name='command')
async def help_command(ctx):
    await ctx.send('```Commands:\n!ask [question]\n!roll [xdy]\n!clearbot [amount]\n!clearuser [user] [amount]\n!help```')

@client.command(name="clearall")
async def clearall_command(ctx):
    await clear_all.clearall_command(ctx)

@client.command(name='reddit')
async def meme(ctx, message):
    await reddit.meme(ctx, message)

client.run(DISCORD_TOKEN)