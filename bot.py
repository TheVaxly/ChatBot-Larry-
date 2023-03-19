from discord.ext import commands
import discord
import clear_all, clear_user, roll, reddit, ask
import asyncio

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

dice_history = []
symbol = "```"

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="rule34"))

@client.command(name='ask')
async def ask_command(ctx, *, user_input="Tell me a joke"):
    await ask.ask_command(ctx, user_input=user_input)

@client.command(name='roll')
async def roll_command(ctx, *, dice: str = ''):
    await roll.roll_command(ctx, dice=dice)

@client.command(name='clearbot')
async def clear_command(ctx, amount: int):
    bot_messages = []
    async for message in ctx.channel.history(limit=None):
        if message.author == client.user:
            bot_messages.append(message)
    to_delete = min(amount, len(bot_messages))
    if to_delete <= 0:
        await ctx.send("``Invalid amount.``")
        return
    for i in range(to_delete):
        await bot_messages[i].delete()
    await ctx.send(f"``{to_delete} bot messages have been deleted.``")
    print(f'{ctx.author.name} deleted {to_delete} bot messages')

@client.command(name='clearuser')
async def clearuser_command(ctx, user: discord.Member = None, amount: int = None):
    await clear_user.clearuser_command(ctx, user, amount)

@client.command(name='command')
async def help_command(ctx):
    await ctx.send('```Commands:\n!ask [question]\n!roll [xdy]\n!clearbot [amount]\n!clearuser [user] [amount]\n!help```')

@client.command(name="clearall")
async def clear_all(ctx):
    # Send a warning message before executing the command
    warning_msg = await ctx.send("Are you sure you want to delete all messages in this channel? This action cannot be undone. Type ``!yes`` to confirm.")
    try:
        # Wait for a response from the user
        async def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "!yes"
        await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within 30 seconds, cancel the command
        await warning_msg.delete()
        await ctx.send("Command canceled. You did not confirm within 30 seconds.")
        return
    else:
        # If the user confirms, delete all messages in the channel
        await warning_msg.delete()
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.guild.me or message.author == ctx.author:
            await message.delete()
    await ctx.send(f"All messages have been deleted.")

    print(f"{ctx.author.name} deleted all messages.")

@client.command(name='reddit')
async def meme(ctx, message):
    await reddit.meme(ctx, message)

client.run(DISCORD_TOKEN)