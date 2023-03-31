import random
import discord

dice_history = []

symbol = '``'

async def roll_command(ctx, *, dice: str = ''):
    if dice == 'last':
        if len(dice_history) < 2:
            await ctx.send('``There is no previous dice roll in the history.``')
            return
        rolls, limit = dice_history[-2:]
        result = sum(random.randint(1, limit) for _ in range(rolls))
        await ctx.send(f'{symbol}{result}{symbol}')
        print(f'{ctx.author.name} rolled {result}')
    else:
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send(embed=discord.Embed(title='Invalid dice format.', description='Please use the format: ``<number of dice>``d``<number of sides>``', color=discord.Color.red()))
            return

        result = sum(random.randint(1, limit) for _ in range(rolls))
        dice_history[-2:] = [rolls, limit]

        await ctx.send(embed=discord.Embed(title=f'```{symbol}{result}{symbol}```', color=discord.Color.gold()))
        print(f'{ctx.author.name} rolled {result}')
        print(f'Dice history: {dice_history}')