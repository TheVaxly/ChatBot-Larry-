import discord
import sqlite3

#Connect to the balances and last_used databases
conn = sqlite3.connect('db/balances.db')
conn_coin = sqlite3.connect('db/coin.db')

# Create the balances table if it doesn't exist
conn.execute('CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)')

conn_coin.execute('''CREATE TABLE IF NOT EXISTS coin
                (user_id INT PRIMARY KEY NOT NULL, balance INT NOT NULL)''')

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
        conn.execute("INSERT INTO balances (user_id, balance) VALUES (?, ?)", (user_id, 100))
        conn.commit()
        return 1000
    else:
        return row[0]

async def chips(ctx, amount: int=None):
    if amount is None:
        await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to exchange.", color=0xff0000))
        return
    chips = amount * 1000
    coin = get_coin(ctx.author.id)
    if amount < 0:
        await ctx.send(embed=discord.Embed(title="Please specify valid amount of coins to exchange.", color=0xff0000))
        return
    if amount > coin:
        await ctx.send(embed=discord.Embed(title="You don't have enough coins to exchange.", color=0xff0000))
        return
    coin -= amount
    conn_coin.execute('UPDATE coin SET balance=? WHERE user_id=?', (coin, ctx.author.id))
    conn_coin.commit()
    balance = get_balance(ctx.author.id)
    balance += chips
    conn.execute('UPDATE balances SET balance=? WHERE user_id=?', (balance, ctx.author.id))
    conn.commit()
    await ctx.send(embed=discord.Embed(title=f"You exchanged {amount} coins for {chips} chips.", color=discord.Color.green()))