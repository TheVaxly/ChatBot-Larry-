import responses
import random
from discord.ext import commands
import requests
import discord
import praw

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
    user_name = ctx.author.name
    channel = ctx.channel.name

    bot_response = responses.send_responses(user_input)

    await ctx.send(symbol + bot_response + symbol)
    print(f'{user_name} asked: {user_input} in #{channel}')

@client.command(name='roll')
async def roll_command(ctx, *, dice: str = ''):
    if dice == 'last':
        if len(dice_history) < 2:
            await ctx.send('```There is no previous dice roll in the history.```')
            return
        rolls, limit = dice_history[-2:]
        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(symbol + result + symbol)
        print(f'{ctx.author.name} rolled {result}')
    else:
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('```Invalid dice format or command.```')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        dice_history[-2:] = [rolls, limit]

        await ctx.send(symbol + result + symbol)
        print(f'{ctx.author.name} rolled {result}')
        print(f'Dice history: {dice_history}')

@client.command(name='clearbot')
async def clear_command(ctx, amount: int):
    bot_messages = []
    async for message in ctx.channel.history(limit=100):
        if message.author == client.user:
            bot_messages.append(message)
    to_delete = min(amount, len(bot_messages))
    if to_delete <= 0:
        await ctx.send("```Invalid amount.```")
        return
    for i in range(to_delete):
        await bot_messages[i].delete()
    print(f'{ctx.author.name} deleted {to_delete} bot messages')

@client.command(name='clearuser')
async def clearuser_command(ctx, user: discord.Member, amount: int):
    messages = []
    async for message in ctx.channel.history(limit=100):
        if message.author == user:
            messages.append(message)
    to_delete = min(amount, len(messages))
    if to_delete <= 0:
        await ctx.send(f"```No messages found for user {user.name}.```")
        return
    for i in range(to_delete):
        await messages[i].delete()
    print(f'{ctx.author.name} deleted {to_delete} messages from {user.name}')

@client.command(name='command')
async def help_command(ctx):
    await ctx.send('```Commands:\n!ask [question]\n!roll [xdy]\n!clearbot [amount]\n!clearuser [user] [amount]\n!help```')

@client.command(name='clearall')
async def clearall_command(ctx):   
    async for message in ctx.channel.history(limit=1000):
        if message.author == client.user or message.author == ctx.author:
            await message.delete()
    print(f'{ctx.author.name} deleted all messages.')

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

    await ctx.send(f'```{random_sub.title}```\n{random_sub.url}')

client.run(DISCORD_TOKEN)
