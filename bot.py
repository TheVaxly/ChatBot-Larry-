import discord
import random
from discord.ext import commands
import praw
from commands.ask import ask_command
from commands.roll import roll_command
from commands.clearbot import clear_command
from commands.clearuser import clearuser_command


DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

dice_history = []

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command(name='ask')
async def ask(ctx, *, question):
    ask_command(ctx, question)

@client.command(name='roll')
async def roll(ctx, dice: str):
    roll_command(ctx, dice)

@client.command(name='clearbot')
async def clearbot(ctx, amount: int):
    clear_command(ctx, amount)

@client.command(name='clearuser')
async def clearuser(ctx, user: discord.Member, amount: int):
    clearuser_command(ctx, user, amount)

@client.command(name='clearall')
async def clearall(ctx):
    clear_command(ctx, 1000)


reddit = praw.Reddit(client_id='Umj3PcYICUCd-F2litkmnw',
                    client_secret='VCIOMQnuko0O3vEdKEBcktS_00yW1g',
                    user_agent='meme:584171:v1.0 (by /u/VaxlyQ)')

@client.command(name='reddit')
async def meme(ctx, message):
    subreddit = reddit.subreddit(message)
    all_subs = []
    hot = subreddit.hot(limit=100)

    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)

    await ctx.send(f'{random_sub.title}\n{random_sub.url}')

client.run(DISCORD_TOKEN)