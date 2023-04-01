from discord.ext import commands
import discord
import commands.roll as roll, commands.reddit as reddit, commands.ask as ask, commands.game as game, commands.bal as bal, commands.free_chips as free_chips
import commands.exchange_chips as exchange_chips, commands.exchange_coins as exchange_coins, commands.shop as shop, commands.leaderboard as leaderboard, commands.blackjack as blackjack
import commands.clearall as clearll, commands.youtube as youtube, commands.addchips as addchips, commands.addcoins as addcoins
import os
from dotenv import load_dotenv
load_dotenv()
from commands.responses import send_responses
import chess
import chess.engine

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

engine = chess.engine.SimpleEngine.popen_uci("path/to/engine")
board = chess.Board()

async def upload_emojis(guild):
    with open("board.png", "rb") as f:
        await guild.create_custom_emoji(name="board", image=f.read())
    with open("pieces/white_king.png", "rb") as f:
        await guild.create_custom_emoji(name=":white_king:", image=f.read())
    with open("pieces/black_king.png", "rb") as f:
        await guild.create_custom_emoji(name=":black_king:", image=f.read())
    with open("pieces/white_queen.png", "rb") as f:
        await guild.create_custom_emoji(name=":white_queen:", image=f.read())
    with open("pieces/black_queen.png", "rb") as f:
        await guild.create_custom_emoji(name=":black_queen:", image=f.read())
    with open("pieces/white_rook.png", "rb") as f:
        await guild.create_custom_emoji(name=":white_rook:", image=f.read())
    with open("pieces/black_rook.png", "rb") as f:
        await guild.create_custom_emoji(name=":black_rook:", image=f.read())
    with open("pieces/white_bishop.png", "rb") as f:
        await guild.create_custom_emoji(name=":white_bishop:", image=f.read())
    with open("pieces/black_bishop.png", "rb") as f:
        await guild.create_custom_emoji(name=":black_bishop:", image=f.read())
    with open("pieces/white_knight.png", "rb") as f:
        await guild.create_custom_emoji(name=":white_knight:", image=f.read())
    with open("pieces/black_knight.png", "rb") as f:
        await guild.create_custom_emoji(name=":black_knight:", image=f.read())

@client.event
async def on_message(message):
    global board, engine
    if message.author == client.user:
        return
    if message.content.startswith('!move'):
        if board.turn == chess.WHITE:
            try:
                move = message.content.split()[1]
                board.push_uci(move)
                result = engine.play(board, chess.engine.Limit(time=2.0))
                board.push(result.move)
                fen = board.fen()
                # Update the board image with the new position
                # Use the custom emojis for each chess piece to display the position
                board_image = f":board:\n:white_king::{fen.split()[0].replace('/', '::')}::black_king:\n:board:"
                await message.channel.send(board_image)
            except:
                await message.channel.send("Invalid move or something went wrong!")
        else:
            await message.channel.send("It's not your turn!")
    elif message.content == '!board':
        fen = board.fen()
        # Display the current board position using the custom emojis
        board_image = f":board:\n:white_king::{fen.split()[0].replace('/', '::')}::black_king:\n:board:"
        await message.channel.send(board_image)


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

@client.command(name='reddit', help="Get a random post from a subreddit")
async def meme(ctx, message=None):
    if message is None:
        await ctx.send(embed=discord.Embed(title="Invalid", description="``Please provide a subreddit.``", color=discord.Color.red()))
        return
    await reddit.meme(ctx, message)

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

# command to play blackjack with individual user balances
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
@commands.has_role('Owner')
async def add_chipsy(ctx, amount: int=None):
    await addchips.add_chips(ctx, amount)

@client.command(name="addcoins", help="Add coins to a user (Admin only)")
@commands.has_role('Owner')
async def add_coinsy(ctx, amount: int=None):
    await addcoins.add_coins(ctx, amount)

client.run(os.getenv('token'))