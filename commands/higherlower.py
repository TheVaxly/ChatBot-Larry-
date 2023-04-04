import json
import random
import asyncio
import discord


async def higherlower(ctx, client):
    with open('db/db.json', 'r') as f:
        data = json.load(f)
    
    # Select two random objects from the list
    obj1, obj2 = random.sample(data["objects"], 2)
    obj1_name, obj1_value = obj1["name"], obj1["value"]
    obj2_name, obj2_value = obj2["name"], obj2["value"]

    player = ctx.author
    list_category_id = []
    category_id = ctx.channel.id
    list_category_id.append(category_id)
    category_channel = client.get_channel(list_category_id[0])
    threads = category_channel.threads

    thread = await category_channel.create_thread(name=f"{player.name} Blackjack", type=discord.ChannelType.public_thread)

    await thread.add_user(player)
    
    # Ask the user to guess if the first object's value is higher or lower than the second object's value
    message = await thread.send(f"Is **{obj1_name}**'s value higher or lower than **{obj2_name}**'s ({obj2_value}) value? Type 'higher' or 'lower'.")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['higher', 'lower', "stop"]
    
    try:
        response = await client.wait_for('message', check=lambda m: m.author == player)
        if response.content.lower() == "stop":
            await thread.send("Game stopped.")
            await asyncio.sleep(10)
            await thread.delete()
            return
    except asyncio.TimeoutError:
        await thread.send("Time's up! You took too long to respond.")
        await asyncio.sleep(10)
        await thread.delete()
        return
    # Determine if the user's guess was correct and send a message with the result
    if (response.content.lower() == 'higher' and obj1_value > obj2_value) or \
       (response.content.lower() == 'lower' and obj1_value < obj2_value):
        await thread.send(f"**Correct!** **{obj2_name}** value is {'higher' if obj2_value > obj1_value else 'lower'} than **{obj1_name}**'s value.")
        obj1_name, obj1_value = obj2_name, obj2_value
    else:
        await thread.send(f"**Sorry!**. It's value is {'higher' if obj2_value > obj1_value else 'lower'} than **{obj1_name}**'s value. **Better luck next time!**")
        await asyncio.sleep(10)
        await thread.delete()
        return
    
    while True:
        if response.content.lower() == "stop":
            await thread.send("Game stopped.")
            await asyncio.sleep(10) 
            await thread.delete()
            return
        # Select a new random object and ask the user to guess if its value is higher or lower than the previous object's value
        obj = random.choice(data["objects"])
        obj_name, obj_value = obj["name"], obj["value"]
        message = await thread.send(f"Is **{obj_name}**'s value higher or lower than **{obj1_name}**'s ({obj1_value}) value? Type 'higher' or 'lower'.")
        
        try:
            # Wait for the user's response
            response = await client.wait_for('message', check=lambda m: m.author == player)
        except asyncio.TimeoutError:
            await thread.send("Time's up! You took too long to respond.")
            await asyncio.sleep(10)
            await thread.delete()
            return
        
        # Determine if the user's guess was correct and send a message with the result
        if (response.content.lower() == 'higher' and obj_value > obj1_value) or \
           (response.content.lower() == 'lower' and obj_value < obj1_value):
            await thread.send(f"**Correct!** **{obj_name}** value is {'higher' if obj_value > obj1_value else 'lower'} than **{obj1_name}**'s value.")
            obj1_name, obj1_value = obj_name, obj_value
        else:
            await thread.send(f"**Sorry!**. It's value is {'higher' if obj_value > obj1_value else 'lower'} than **{obj1_name}**'s value. **Better luck next time!**")
            await asyncio.sleep(10)
            await thread.delete()
            return
