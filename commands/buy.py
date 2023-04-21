import sqlite3
import discord

conn = sqlite3.connect('db/balances.db')

conn.execute('''CREATE TABLE IF NOT EXISTS balances
                (user_id INT PRIMARY KEY NOT NULL, balance INT NOT NULL)''')

conn_coin = sqlite3.connect('db/coin.db')

conn_coin.execute('''CREATE TABLE IF NOT EXISTS coin
                (user_id INT PRIMARY KEY NOT NULL, balance INT NOT NULL)''')

conn_invetory = sqlite3.connect('db/inventory.db')

conn_invetory.execute('''CREATE TABLE IF NOT EXISTS inventory
                (user_id INT PRIMARY KEY NOT NULL, balance INT NOT NULL)''')

def add_inventory(user_id, amount):
    balance = get_inventory(user_id)
    conn_invetory.execute("UPDATE inventory SET balance=? WHERE user_id=?", (balance + amount, user_id))
    conn_invetory.commit()

def get_inventory(user_id):
    cursor = conn_invetory.execute("SELECT balance FROM inventory WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn_invetory.execute("INSERT INTO inventory (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn_invetory.commit()
        return 0
    else:
        return row[0]

def get_coin(user_id):
    cursor = conn_coin.execute("SELECT balance FROM coin WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn_coin.execute("INSERT INTO coin (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn_coin.commit()
        return 0
    else:
        return row[0]
    
def get_balance(user_id):
    cursor = conn.execute("SELECT balance FROM balances WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn.execute("INSERT INTO balances (user_id, balance) VALUES (?, ?)", (user_id, 1000))
        conn.commit()
        return 1000
    else:
        return row[0]
    
def add_balance(user_id, amount):
    balance = get_balance(user_id)
    new_balance = balance + amount
    conn.execute("UPDATE balances SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()

def add_coin(user_id, amount):
    coin_balance = get_coin(user_id)
    new_balance = coin_balance + amount
    conn_coin.execute("UPDATE coin SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn_coin.commit()

def remove_balance(user_id, amount):
    balance = get_balance(user_id)
    new_balance = balance - amount
    conn.execute("UPDATE balances SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()

def remove_coin(user_id, amount):
    coin_balance = get_coin(user_id)
    new_balance = coin_balance - amount
    conn_coin.execute("UPDATE coin SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn_coin.commit()

items_fishbaits = {
    "basic": {
        "name": "Basic Fishbait",
        "price": 1000,
    },
    "advanced": {
        "name": "Advanced Fishbait",
        "price": 2500,
    },
    "master": {
        "name": "Master Fishbait",
        "price": 5000,
    },
    "legendary": {
        "name": "Legendary Fishbait",
        "price": 7500,
    },
    "mythical": {
        "name": "Mythical Fishbait",
        "price": 10000,
    },
    "godly": {
        "name": "Godly Fishbait",
        "price": 15000,
    },
    "ultimate": {
        "name": "Ultimate Fishbait",
        "price": 20000,
    },
    "sus": {
        "name": "Sus Fishbait",
        "price": 100000,
    },
}

async def buys(ctx, item):
    if item == None:
        embed = discord.Embed(title="You didn't provide an item", description=f"Please provide an item to buy", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.name}" )
        await ctx.send(embed=embed)
        return
    if item != None:
        if item == "basic":
            if get_balance(ctx.author.id) >= items_fishbaits["basic"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["basic"]["price"])
                add_inventory(ctx.author.id, 1)
                embed = discord.Embed(title="You bought a basic fishbait", description=f"You now have {get_inventory(ctx.author.id)} basic fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['basic']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)

        if item == "advanced":
            if get_balance(ctx.author.id) >= items_fishbaits["advanced"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["advanced"]["price"])
                add_inventory(ctx.author.id, 2)
                embed = discord.Embed(title="You bought a advanced fishbait", description=f"You now have {get_inventory(ctx.author.id)} advanced fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['advanced']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "master":
            if get_balance(ctx.author.id) >= items_fishbaits["master"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["master"]["price"])
                add_inventory(ctx.author.id, 3)
                embed = discord.Embed(title="You bought a master fishbait", description=f"You now have {get_inventory(ctx.author.id)} master fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['master']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "legendary":
            if get_balance(ctx.author.id) >= items_fishbaits["legendary"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["legendary"]["price"])
                add_inventory(ctx.author.id, 4)
                embed = discord.Embed(title="You bought a legendary fishbait", description=f"You now have {get_inventory(ctx.author.id)} legendary fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['legendary']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "mythical":
            if get_balance(ctx.author.id) >= items_fishbaits["mythical"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["mythical"]["price"])
                add_inventory(ctx.author.id, 5)
                embed = discord.Embed(title="You bought a mythical fishbait", description=f"You now have {get_inventory(ctx.author.id)} mythical fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['mythical']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "godly":
            if get_balance(ctx.author.id) >= items_fishbaits["godly"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["godly"]["price"])
                add_inventory(ctx.author.id, 6)
                embed = discord.Embed(title="You bought a godly fishbait", description=f"You now have {get_inventory(ctx.author.id)} godly fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['godly']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "ultimate":
            if get_balance(ctx.author.id) >= items_fishbaits["ultimate"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["ultimate"]["price"])
                add_inventory(ctx.author.id, 7)
                embed = discord.Embed(title="You bought a ultimate fishbait", description=f"You now have {get_inventory(ctx.author.id)} ultimate fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['ultimate']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

        if item == "sus":
            if get_balance(ctx.author.id) >= items_fishbaits["sus"]["price"]:
                remove_balance(ctx.author.id, items_fishbaits["sus"]["price"])
                add_inventory(ctx.author.id, 8)
                embed = discord.Embed(title="You bought a sus fishbait", description=f"You now have {get_inventory(ctx.author.id)} sus fishbaits", color=discord.Color.green())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You don't have enough money", description=f"You need {items_fishbaits['sus']['price'] - get_balance(ctx.author.id)} more money to buy this item", color=discord.Color.red())
                embed.set_footer(text=f"Requested by {ctx.author.name}" )
                await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="That item doesn't exist", description=f"Use ``!shop`` to see the items", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.name}" )
        await ctx.send(embed=embed)