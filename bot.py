import discord
import responses
import random
from discord.ext import commands
import googlesearch

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

dice_history = []

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command(name='ask')
async def ask_command(ctx, *, user_input):
    user_name = ctx.author.name
    channel = ctx.channel.name

    bot_response = responses.send_responses(user_input)

    await ctx.send(bot_response)
    print(f'{user_name} asked: {user_input} in #{channel}')

@client.command(name='roll')
async def roll_command(ctx, *, dice: str = ''):
    if dice == 'last':
        if len(dice_history) < 2:
            await ctx.send('There is no previous dice roll in the history.')
            return
        rolls, limit = dice_history[-2:]
        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(result)
        print(f'{ctx.author.name} rolled {result}')
    else:
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Invalid dice format or command.')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        dice_history[-2:] = [rolls, limit]

        await ctx.send(result)
        print(f'{ctx.author.name} rolled {result}')
        print(f'Dice history: {dice_history}')

client.run(DISCORD_TOKEN)
