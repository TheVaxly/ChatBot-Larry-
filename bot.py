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

engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")

async def send_board(ctx, board):
    img = chess.svg.board(board)
    img = img.replace("#FFFFFF", "#FFCE9E").replace("#D18B47", "#AA5500")
    with open("board.svg", "w", encoding="utf-8") as f:
        f.write(img)
    with open("board.svg", "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@client.command(name='chess', help='Play chess against the bot')
async def chess(ctx, color='w', time_limit=5):
    if color == 'w':
        human_color = chess.WHITE
    elif color == 'b':
        human_color = chess.BLACK
    else:
        await ctx.send('Invalid color choice. Please choose "w" for white or "b" for black.')
        return
    
    board = chess.Board()
    await send_board(ctx, board)
    while not board.is_game_over():
        if board.turn == human_color:
            await ctx.send(f'Your move ({color}):')
            def check_move(m):
                try:
                    board.push_san(m.content)
                    return True
                except ValueError:
                    return False
            move = await client.wait_for('message', check=check_move, timeout=time_limit*60)
            board.push_san(move.content)
        else:
            result = engine.play(board, chess.engine.Limit(time=time_limit))
            board.push(result.move)
            await ctx.send(f'The bot played {result.move.uci()}')
        await send_board(ctx, board)
        
    result = board.result()
    if result == "1-0":
        winner = 'White'
    elif result == "0-1":
        winner = 'Black'
    else:
        winner = 'No one (draw)'
    await ctx.send(f'{winner} wins!')
    
    # Offer to save the game in PGN format
    def check_save(m):
        return m.content.lower() in ['y', 'n']
    await ctx.send('Would you like to save the game in PGN format? (y/n)')
    save_response = await client.wait_for('message', check=check_save)
    if save_response.content.lower() == 'y':
        game_name = f'chess-{ctx.message.created_at.strftime("%Y%m%d-%H%M%S")}.pgn'
        with open(game_name, 'w') as f:
            f.write(board.board_fen())

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