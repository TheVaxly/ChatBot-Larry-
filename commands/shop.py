import discord
from discord.ext import commands
import asyncio

async def shopy(ctx, client):
    page_one = discord.Embed(title="Shop", description="Use Larry coins to buy items", color=0x00ff00)
    page_one.add_field(name="10 Larry coins", value="Item 1\nItem 2\nItem 3", inline=False)
    page_one.add_field(name="25 Larry coins", value="Item 4\nItem 5\nItem 6", inline=False)
    page_one.set_footer(text="Page 1/2")

    page_two = discord.Embed(title="Shop", description="Use Larry coins to buy items", color=0x00ff00)
    page_two.add_field(name="50 Larry coins", value="Item 7\nItem 8\nItem 9", inline=False)
    page_two.add_field(name="75 Larry coins", value="Item 10\nItem 11\nItem 12", inline=False)
    page_two.set_footer(text="Page 2/2")

    pages = [page_one, page_two]

    message = await ctx.send(embed=page_one)
    current_page = 0
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '➡️' and current_page < len(pages)-1:
                current_page += 1
                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '⬅️' and current_page > 0:
                current_page -= 1
                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.clear_reactions()
            break