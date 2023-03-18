import responses

async def ask_command(ctx, *, user_input):
    user_name = ctx.author.name
    channel = ctx.channel.name

    bot_response = responses.send_responses(user_input)
    symbol = "```"

    if "code" or "program" or "python" or "pygame" or "javascript" or "html" or "c#" or "c++" or "js" or "php" in bot_response:
        bot_response = symbol + bot_response + symbol

    await ctx.send(bot_response)
    print(f'{user_name} asked: {user_input} in #{channel}')