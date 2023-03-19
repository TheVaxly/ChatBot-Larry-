import discord

async def clearall_command(ctx):
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.guild.me or message.author == ctx.author:
            await message.delete()
    await ctx.send(f"@everyone")
    await ctx.send(f"```All messages have been deleted.```")

    print(f"{ctx.author.name} deleted all messages.")