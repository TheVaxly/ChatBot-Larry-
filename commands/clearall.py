import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

async def clearall_command(ctx):   
    async for message in ctx.channel.history(limit=1000):
        if message.author == client.user or message.author == ctx.author:
            await message.delete()
    print(f'{ctx.author.name} deleted all messages.')