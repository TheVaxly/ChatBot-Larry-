import json
import random
import asyncio
import discord

used = 0
used2 = 0
new_object = []
new_object_value = []

# Load data from db.json file
with open('db/db.json', 'r') as f:
    data = json.load(f)

# Function to generate a new question
def get_question():
    global used, used2, new_object, new_object_value
    # Choose two random objects
    obj1, obj2 = random.sample(data["objects"], 2)
    object1, object1_value = obj1["name"], obj1["value"]
    object2, object2_value = obj2["name"], obj2["value"]
    # Check if the attribute value for object1 is higher or lower than object2
    if used == 0:
        if object1_value > object2_value:
            answer = 'higher'
        else:
            answer = 'lower'
    elif used == 1:
        if new_object_value[used2] > object2_value:
            answer = 'higher'
        else:
            answer = 'lower'
    if used == 0:
        question = discord.Embed(title=f'Is {object1}\'s {object1_value:,} value higher or lower than {object2}\'s value?', color=discord.Color.green())
        used += 1
        new_object.append(object2)
        new_object_value.append(object2_value)
        print(new_object, new_object_value)
    elif used == 1:
        question = discord.Embed(title=f'Is {new_object[used2]}\'s {new_object_value[used2]:,} value higher or lower than {object2}\'s value?', color=discord.Color.green())
        used2 += 1
        new_object.append(object2)
        new_object_value.append(object2_value)
        print(new_object, new_object_value)

    return question, answer

async def on_message(ctx, client):
        channel = ctx.channel
        player = ctx.author
        question, answer = get_question()
        thread = await channel.create_thread(name=f"{player.name}'s Higher or Lower Game", type=discord.ChannelType.public_thread)
        await thread.add_user(player)
        await thread.send(embed=question)
        
        # Game loop
        while True:
            # Wait for player input
            try:
                player_input = await client.wait_for('message', check=lambda m: m.author == player, timeout=10*60)
            except asyncio.TimeoutError:
                await thread.send(embed=discord.Embed(title="Timed out.", description="``You took too long to respond.``", color=discord.Color.red()))
                await asyncio.sleep(10)
                await thread.delete()
                break
            
            # Check if player surrenders
            if player_input.content.lower() == 'surrender':
                await thread.send(embed=discord.Embed(title="Game over", description=f"You surrendered. The correct answer was {answer}.", color=discord.Color.gold()))
                await asyncio.sleep(10)
                await thread.delete()
                break
            
            # Check if player answer is correct
            if player_input.content.lower() == answer:
                await thread.send(embed=discord.Embed(title="Correct!", description=f"The correct answer was {answer}.", color=discord.Color.green()))
                question, answer = get_question()
                await thread.send(embed=question)
            elif player_input.content.lower() == "lower" or player_input.content.lower() == "higher" and player_input.content.lower() != answer:
                used = 0
                used2 = 0
                del new_object[:]
                del new_object_value[:]
                await thread.send(embed=discord.Embed(title="Incorrect!", description=f"The correct answer was {answer}.", color=discord.Color.red()))
                await asyncio.sleep(10)
                await thread.delete()
                break
            else:
                continue