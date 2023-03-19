import discord


async def clearuser_command(ctx, user: discord.Member = None, amount: int = None):
    try:
        if user is None:
            await ctx.send("``Please specify a user.``")
            return
        elif amount is None:
            await ctx.send("``Please specify the number of messages to delete.``")
            return

        messages = []
        async for message in ctx.channel.history(limit=None):
            if message.author == user:
                messages.append(message)
        to_delete = min(amount, len(messages))
        if to_delete <= 0:
            await ctx.send(f"``Invalid amount.``")
            return
        elif to_delete > 100:
            await ctx.send(f"``Maximum number of messages that can be deleted is 100.``")
            return
        
        for i in range(to_delete):
            await messages[i].delete()

        await ctx.send(f"{to_delete} messages from {user.mention} have been deleted.")
    except Exception:
        await ctx.send("``An error occurred while deleting messages.``")
        return
    print(f'{ctx.author.name} deleted {to_delete} messages from {user.name}')