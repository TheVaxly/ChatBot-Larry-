import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY
model_engine = "davinci"

memory = {}

client = discord.Client()

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

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )

        bot_response = response.choices[0].text.strip()
        await message.channel.send(bot_response)

client.run(DISCORD_TOKEN)