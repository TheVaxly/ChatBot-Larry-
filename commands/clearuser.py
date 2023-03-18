import discord


async def clearuser_command(ctx, user: discord.Member, amount: int):
    messages = []
    async for message in ctx.channel.history(limit=100):
        if message.author == user:
            messages.append(message)
    to_delete = min(amount, len(messages))
    if to_delete <= 0:
        await ctx.send(f"No messages found for user {user.name}.")
        return
    for i in range(to_delete):
        await messages[i].delete()
    print(f'{ctx.author.name} deleted {to_delete} messages from {user.name}')
