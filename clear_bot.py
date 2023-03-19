import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

async def clear_command(ctx, amount: int):
    bot_messages = []
    async for message in ctx.channel.history(limit=100):
        if message.author == client.user:
            bot_messages.append(message)
    to_delete = amount
    if to_delete <= 0:
        await ctx.send("```Invalid amount.```")
        return
    for i in range(to_delete):
        await bot_messages[i].delete()
    print(f'{ctx.author.name} deleted {to_delete} bot messages')