import commands.responses as responses
import discord

symbol = "```"

async def ask_command(ctx, *, user_input):
    try:
        user_name = ctx.author.name
        channel = ctx.channel.name

        bot_response = responses.send_responses(user_input)

        await ctx.send(symbol + bot_response + symbol)
    except Exception:
        await ctx.send(embed=discord.Embed(title="error", color=discord.Color.red()))
        return
    print(f'{user_name} asked: {user_input} in #{channel}')