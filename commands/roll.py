import random

dice_history = []

async def roll_command(ctx, *, dice: str = ''):
    if dice == 'last':
        if len(dice_history) < 2:
            await ctx.send('There is no previous dice roll in the history.')
            return
        rolls, limit = dice_history[-2:]
        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(result)
        print(f'{ctx.author.name} rolled {result}')
    else:
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Invalid dice format or command.')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        dice_history[-2:] = [rolls, limit]

        await ctx.send(result)
        print(f'{ctx.author.name} rolled {result}')
        print(f'Dice history: {dice_history}')
