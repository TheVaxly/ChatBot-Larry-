import discord
import openai

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

memory = {}

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

        if message.channel.id not in memory:
            memory[message.channel.id] = []

        prev_inputs = memory[message.channel.id]
        prompt = '\n'.join(prev_inputs + [user_input])
        memory[message.channel.id].append(user_input)
        user_name = message.author.name
        channel = message.channel.name

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )

        bot_response = response.choices[0].text.strip()
        await message.channel.send(bot_response)
        print(f'{user_name} asked: {user_input} in #{channel}')

client.run(DISCORD_TOKEN)