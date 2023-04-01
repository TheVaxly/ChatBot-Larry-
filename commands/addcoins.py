import sqlite3
import discord
from discord.ext import commands

conn = sqlite3.connect("db/coin.db")

def update_balance(user_id, amount):
    cursor = conn.execute("SELECT balance FROM coin WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    balance = row[0] + amount
    conn.execute("UPDATE coin SET balance=? WHERE user_id=?", (balance, user_id))
    conn.commit()

async def add_coins(ctx, amount):
        if amount is None:
            await ctx.send(embed=discord.Embed(title="Please specify an amount of coins to add.", color=0xff0000))
            return
        user = ctx.message.author
        user_id = user.id
        update_balance(user_id, amount)
        await ctx.send(embed=discord.Embed(title="Success", description=f"``Added {amount} coins to {user.name}``", color=discord.Color.green()))
