import random
import discord

async def game(ctx, message):
    if message == None:
        await ctx.send(embed=discord.Embed(title="Invalid move", description="``Please specify a choice.``", color=discord.Color.red()))
        return
    options = ["rock", "paper", "scissors"]
    computer_choice = random.choice(options)
    result = f"You chose {message} and the Larry chose {computer_choice}."
    if message not in options:
        await ctx.send("``Invalid input.``")
    else:
        if message == computer_choice:
            await ctx.send(embed=discord.Embed(title="It's a tie!", description=f"{result}", color=discord.Color.gold()))
        elif message == "rock" and computer_choice == "scissors":
            await ctx.send(embed=discord.Embed(title="You win!", description=f"{result}", color=discord.Color.green()))
        elif message == "paper" and computer_choice == "rock":
            await ctx.send(embed=discord.Embed(title="You win!", description=f"{result}", color=discord.Color.green()))
        elif message == "scissors" and computer_choice == "paper":
            await ctx.send(embed=discord.Embed(title="You win!", description=f"{result}", color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(title="You lose!", description=f"{result}", color=discord.Color.red()))