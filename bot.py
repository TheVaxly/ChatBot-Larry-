import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from commands.responses import send_responses
import commands.card as card, commands.cards as cards
import os, commands.higherlower as higherlower, commands.buy as buy, sqlite3, commands.cards as cards
import commands.clearall as clearll, commands.youtube as youtube, commands.addchips as addchips, commands.addcoins as addcoins, commands.news as news
import commands.roll as roll, commands.ask as ask, commands.game as game, commands.bal as bal, commands.free_chips as free_chips
import commands.exchange_chips as exchange_chips, commands.exchange_coins as exchange_coins, commands.shop as shop, commands.leaderboard as leaderboard, commands.blackjack as blackjack
import commands.reddit as reddit
load_dotenv()

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="rule34"))
    await client.tree.sync()

@client.command(name='ask', help="Ask the bot a question")
async def ask_command(ctx, *, user_input="Tell me a joke"):
    await ask.ask_command(ctx, user_input=user_input)

@client.command(name='roll', help="Roll a dice (xdy)")
async def roll_command(ctx, *, dice: str = ''):
    await roll.roll_command(ctx, dice=dice)

@client.command(name="clearall", help="Delete all messages in a channel (Admin only)")
@commands.has_role('Owner')
async def clear_alls(ctx, client=client):
    await clearll.clear_all(ctx, client=client)

@client.command(name='subs', help="Get the subscriber count of a channel (Probs doesn't work)")
async def subscribersy(ctx, user_input):
    await youtube.subscribers(ctx, user_input)

@client.tree.command(name='larry', description="Ask bot yes very many uwu")
@discord.app_commands.describe(question='What do you want to ask the bot? uwu')
async def larry(int: discord.Interaction, question: str):
    try:
        await int.response.defer(thinking=True)
        bot_response = send_responses(question)
        await int.followup.send(content=f'Question: {question}\n```{bot_response}```')
    except Exception:
        print(f"Err: {Exception}")
        return

@client.command(name='rps', help="Play rock paper scissors")
async def rps(ctx, message=None):
    await game.game(ctx, message)

@client.command(name='blackjack', help="Play blackjack")
async def blackjacks(ctx, bet: int=0, client=client):
    await blackjack.blackjack(ctx, bet, client)

@client.command(name='bal', help="Check your Blackjack balance")
async def balance(ctx):
    await bal.balance(ctx)

@client.command(name='leaderboard', help="Check the Blackjack leaderboard")
async def leaderboardy(ctx, client=client):
    await leaderboard.leaderboard(ctx, client)

@client.command(name="daily", help="Get 1000 chips once per day")
async def once_per_day(ctx):
    await free_chips.once_per_day(ctx)

@client.command(name="weekly", help="Get 5000 chips once per week")
async def once_per_day(ctx):
    await free_chips.once_per_week(ctx)

@client.command(name="coins", help="Exchange your chips for Larry coins")
async def coins(ctx, amount: int=None):
    await exchange_coins.coins(ctx, amount)

@client.command(name="chips", help="Exchange your Larry coins for chips")
async def chips(ctx, amount: int=None):
    await exchange_chips.chips(ctx, amount)

@client.command(name="shop", help="Use Larry coins to buy items")
async def shops(ctx, client=client):
    await shop.shopy(ctx, client)

@client.command(name="addchips", help="Add chips to a user (Admin only)")
async def add_chipsy(ctx, amount: int=None):
    await addchips.add_chips(ctx, amount)

@client.command(name="addcoins", help="Add coins to a user (Admin only)")
@commands.has_role('Cheats')
async def add_coinsy(ctx, amount: int=None):
    await addcoins.add_coins(ctx, amount)

@client.command(name="helpjack", help="Get help with blackjack")
async def blackjack_help(ctx):
    await ctx.send(embed=discord.Embed(title="Blackjack Help", description="``!blackjack <bet> - start the game``\n``hit - get 1 more card``\n``stand - finish your turn``\n``double - double your bet and finish your turn``\n``split - split the cards with same value``\n``surrender - leave the game (you lose half the bet)``\n``!helpjack - this command``", color=discord.Color.green()))

@client.command(name="news", help="Get the latest news on Delfi or Postimees!")
async def newy(ctx, newsq: str=None):
    if newsq is None:
        ran = random.randint(1, 2)
        if ran == 1:
            await news.news_postimees(ctx)
        elif ran == 2:
            await news.news_delfi(ctx)
    if newsq == "postimees":
        await news.news_postimees(ctx)
    elif newsq == "delfi":
        await news.news_delfi(ctx)

@client.command(name="yt", help="Get the youtube video")
async def youtubey(ctx, url):
    await youtube.youtube(ctx, url)

@client.command(name="hl", help="Play higher or lower")
async def higherlowery(ctx, client=client):
    await higherlower.on_message(ctx, client)


@client.command(name="img", help="Get an image from Larry")
async def img(ctx, *, user_input="Red impostor"):
    await ask.img(ctx, user_input=user_input)

@client.command(name="highscore", help="Check your higher or lower highscore")
async def points(ctx):
    await higherlower.pointsy(ctx)

@client.command(name="buy", help="Buy an item from the shop")
async def buyy(ctx, item: str=None, amount: int=1):
    await buy.buy(ctx, item, amount)

# Create the database connection
conn = sqlite3.connect('db/inv.db')

@client.command(name="inv", help="Check your inventory")
async def inv(ctx):
    user_id = str(ctx.author.id)
    c = conn.cursor()
    c.execute("SELECT * FROM inv WHERE user_id=?", (user_id,))
    row = c.fetchone()

    if row is None:
        await ctx.send("You don't have any items in your inventory.")
    else:
        # Create an embed message
        embeds = discord.Embed(title=f"{ctx.author.name}'s inventory", color=discord.Color.gold())

        # Loop through each item in the inventory and add it to the embed
        items = ["basic", "advanced", "master", "legendary", "mythical", "ultimate", "sus"]
        for item in items:
            amount = row[items.index(item) + 1]
            embeds.add_field(name=item, value=amount, inline=True)

        await ctx.send(embed=embeds)

@client.command(name="sell", help="Sell an item from your inventory")
async def selly(ctx, item: str=None, amount: int=1):
    await buy.sell(ctx, item, amount)

@client.command(name="cards", help="Check your cards")
async def view_cards(ctx, arg=None):
    if arg == "all":
        await cards.carddd(ctx)
    elif arg is None:
        await card.view_collection(ctx)
    else:
        return

@client.command(name="addcard", help="Add a card to your collection")
async def addcardy(ctx, card_id: int):
    await card.add_card(ctx, card_id)

@client.command(name="reddit", help="!reddit <subreddit> [sort] [time] [type] - Fetches a post. Sort: hot(d),new,top,rising,best. Time(top only): hour,day(d),week,month,year,all. Type: image,video,gallery,all(d).")
async def reddity(ctx, subreddit: str, *args):
    await reddit.reddit(ctx, subreddit, *args)

client.run(os.getenv('token'))