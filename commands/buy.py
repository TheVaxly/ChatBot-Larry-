import discord
import sqlite3

# Create the database connection
conn = sqlite3.connect('db/inv.db')
conn.execute('CREATE TABLE IF NOT EXISTS inv (user_id INTEGER PRIMARY KEY, basic INTEGER DEFAULT 0, advanced INTEGER DEFAULT 0, master INTEGER DEFAULT 0, legendary INTEGER DEFAULT 0, mythical INTEGER DEFAULT 0, ultimate INTEGER DEFAULT 0, sus INTEGER DEFAULT 0)')
conn.commit()

conn_bal = sqlite3.connect('db/coin.db')

# Define the list of items with their prices
ITEMS = {
    'basic': 1,
    'advanced': 3,
    'master': 5,
    'legendary': 8,
    'mythical': 10,
    'ultimate': 20,
    'divine': 50,
    'sus': 100
}

def inv_add(user_id, item, amount):
    cursor = conn.execute(f"SELECT {item} FROM inv WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn.execute(f"INSERT INTO inv (user_id, {item}) VALUES (?, ?)", (user_id, amount))
        conn.commit()
    else:
        conn.execute(f"UPDATE inv SET {item}=? WHERE user_id=?", (row[0] + amount, user_id))
        conn.commit()
    
async def buy(ctx, item: str, amount: int):
    # Get the user's balance from the database
    user_id = str(ctx.author.id)
    c = conn_bal.cursor()
    c.execute("SELECT balance FROM coin WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row is None:
        conn_bal.execute("INSERT INTO coin (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn_bal.commit()
        return 0
    balance = row[0]

    # Check if the item exists and the user has enough balance
    if item not in ITEMS:
        await ctx.send(embed=discord.Embed(title="Error", description=f"{item} is not a valid item.", color=0xff0000))
        return
    price = ITEMS[item] * amount
    if balance < price:
        await ctx.send(embed=discord.Embed(title="Error", description=f"You do not have enough coins to buy {amount} {item}.", color=0xff0000))
        return

    # Update the user's balance and inventory in the database
    new_balance = balance - price
    c.execute("UPDATE coin SET balance=? WHERE user_id=?", (new_balance, user_id))
    inv_add(user_id, item, amount)
    conn_bal.commit()

    # Send a confirmation message
    await ctx.send(embed=discord.Embed(title="Success", description=f"You have bought {amount} {item} for {price} coin. Your new balance is {new_balance} coins.", color=0x00ff00))

async def sell(ctx, item, amount):
    # Get the user's balance from the database
    user_id = str(ctx.author.id)
    c = conn_bal.cursor()
    c.execute("SELECT balance FROM coin WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row is None:
        conn_bal.execute("INSERT INTO coin (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn_bal.commit()
        return 0
    balance = row[0]

    # Check if the item exists and the user has enough balance
    if item not in ITEMS:
        await ctx.send(embed=discord.Embed(title="Error", description=f"{item} is not a valid item.", color=0xff0000))
        return
    price = ITEMS[item] * amount
    cursor = conn.execute(f"SELECT {item} FROM inv WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        await ctx.send(embed=discord.Embed(title="Error", description=f"You do not have any {item}.", color=0xff0000))
        return
    if row[0] == 0:
        await ctx.send(embed=discord.Embed(title="Error", description=f"You do not have any {item}.", color=0xff0000))
        return
    else:
        if row[0] < amount:
            await ctx.send(embed=discord.Embed(title="Error", description=f"You do not have {amount} {item} to sell.", color=0xff0000))
            return

    # Update the user's balance and inventory in the database
    new_balance = balance + price
    c.execute("UPDATE coin SET balance=? WHERE user_id=?", (new_balance, user_id))
    inv_add(user_id, item, -amount)
    conn_bal.commit()

    # Send a confirmation message
    await ctx.send(embed=discord.Embed(title="Success", description=f"You have sold {amount} {item} for {price} coin. Your new balance is {new_balance} coins.", color=0x00ff00))