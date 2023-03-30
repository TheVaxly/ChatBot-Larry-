import random

async def game(ctx, message):
    options = ["rock", "paper", "scissors"]
    computer_choice = random.choice(options)
    result = f"You chose {message} and the Larry chose {computer_choice}."
    if message not in options:
        await ctx.send("``Invalid input.``")
    else:
        if message == computer_choice:
            await ctx.send(f"``{result} It's a tie!``")
        elif message == "rock" and computer_choice == "scissors":
            await ctx.send(f"``{result} You win!``")
        elif message == "paper" and computer_choice == "rock":
            await ctx.send(f"``{result} You win!``")
        elif message == "scissors" and computer_choice == "paper":
            await ctx.send(f"``{result} You win!``")
        else:
            await ctx.send(f"``{result} You lose!``")