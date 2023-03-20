import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

async def clear_all(ctx):
    warning_msg = await ctx.send("Are you sure you want to delete all messages in this channel? This action cannot be undone. Type ``!yes`` to confirm.")
    try:
        async def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "!yes"
        await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await warning_msg.delete()
        await ctx.send("Command canceled. You did not confirm within 30 seconds.")
        return
    else:
        await warning_msg.delete()
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.guild.me or message.author == ctx.author:
            await message.delete()
    await ctx.send(f"``All messages have been deleted.``")

    print(f"{ctx.author.name} deleted all messages.")