import discord
import responses

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask'):
        user_input = message.content[5:].strip()

        user_name = message.author.name
        channel = message.channel.name

        bot_response = responses.send_responses(user_input)

        await message.channel.send(bot_response)
        print(f'{user_name} asked: {user_input} in #{channel}')

client.run(DISCORD_TOKEN)