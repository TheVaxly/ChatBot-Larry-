import discord
import sqlite3

#Connect to the balances and last_used databases
conn = sqlite3.connect('db/balances.db')
conn_last_used = sqlite3.connect('db/last_used.db')
conn_last_week = sqlite3.connect('db/last_week.db')
conn_coin = sqlite3.connect('db/coin.db')

# Create the balances table if it doesn't exist
conn.execute('CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)')

# Create the last_used table if it doesn't exist
conn_last_used.execute('CREATE TABLE IF NOT EXISTS last_used (user_id INTEGER PRIMARY KEY, last_used TEXT)')

# Create the last_week table if it doesn't exist
conn_last_week.execute('CREATE TABLE IF NOT EXISTS last_week (user_id INTEGER PRIMARY KEY, last_week TEXT)')

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

async def coins(ctx, amount: int=None):
    if amount < 1000:
        await ctx.send(embed=discord.Embed(title="You must exchange at least 1000 chips.", color=0xff0000))
        return
    if amount % 1000 != 0:
        await ctx.send(embed=discord.Embed(title="You can only exchange in multiples of 1000 chips.", color=0xff0000))
        return
    coins = amount // 1000
    coin = get_coin(ctx.author.id)
    coinss = coin + coins
    if amount is None:
        await ctx.send(embed=discord.Embed(title="Please specify an amount of chips to exchange.", color=0xff0000))
        return
    if amount < 0:
        await ctx.send(embed=discord.Embed(title="Please specify valid amount of chips to exchange.", color=0xff0000))
        return
    balance = get_balance(ctx.author.id)
    if amount > balance:
        await ctx.send(embed=discord.Embed(title="You don't have enough chips to exchange.", color=0xff0000))
        return
    balance -= amount
    conn.execute('UPDATE balances SET balance=? WHERE user_id=?', (balance, ctx.author.id))
    conn.commit()
    conn_coin.execute('UPDATE coin SET balance=? WHERE user_id=?', (coinss, ctx.author.id))
    conn_coin.commit()
    await ctx.send(embed=discord.Embed(title=f"You exchanged {amount} chips for {coins} coins.", color=0xff0000))