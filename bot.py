from discord.ext import commands
import discord
import commands.roll as roll, commands.reddit as reddit, commands.ask as ask, commands.game as game, commands.bal as bal, commands.free_chips as free_chips
import commands.exchange_chips as exchange_chips, commands.exchange_coins as exchange_coins, commands.shop as shop, commands.leaderboard as leaderboard, commands.blackjack as blackjack
import commands.clearall as clearll
import os
from dotenv import load_dotenv
load_dotenv()
from commands.responses import send_responses
from googleapiclient.discovery import build

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

@client.command(name='reddit', help="Get a random post from a subreddit")
async def meme(ctx, message=None):
    if message is None:
        await ctx.send(embed=discord.Embed(title="Invalid", description="``Please provide a subreddit.``", color=discord.Color.red()))
        return
    await reddit.meme(ctx, message)

@client.command(name='subs', help="Get the subscriber count of a channel (Probs doesn't work)")
async def subscribers(ctx, *, user_input):
    try:    
        api_service_name = "youtube"
        api_version = "v3"
        key=os.getenv("key")
        youtube = build(api_service_name, api_version, developerKey=key)
        request = youtube.channels().list(part="statistics", forUsername=user_input)
        response = request.execute()
        print(response)
        subscirbers = response["items"][0]["statistics"]["subscriberCount"]
        await ctx.send(f"``{user_input} has {subscirbers} subscribers``")
    except Exception:
        await ctx.send("``No subscribers count found.``")
        return

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
    if message == None:
        await ctx.send(embed=discord.Embed(title="Invalid move", description="``Please specify a choice.``", color=discord.Color.red()))
        return  
    else:
        await game.game(ctx, message)

@client.command(name='blackjack', help="Play blackjack")
async def blackjack(ctx, bet: int):
    bets = bet * 1.5 + bet
    bets = int(bets)
    bets2 = bet + bet
    chips = []
    chips.append(bet)
    # check if the player has enough money to place the bet
    if bet > 0 and bet <= 100:
        # create a deck of cards
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)

            # deal the cards
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            # calculate the value of the hands
            player_value = calculate_hand(player_hand)
            dealer_value = calculate_hand(dealer_hand)

        # let the player take their turn
        while True:
            # show the player's hand and ask for their move
            await ctx.send(f"``Your hand: {', '.join(card[0] + ' of ' + card[1] for card in player_hand)}``")
            await ctx.send(f"``Dealer's hand: {dealer_hand[0][0]} of {dealer_hand[0][1]}, HIDDEN CARD``")
            move = await client.wait_for('message', check=lambda m: m.author == ctx.author)

            # handle the player's move
            if move.content.lower() == "!hit":
                # draw a card and add it to the player's hand
                player_hand.append(deck.pop())
                player_value = calculate_hand(player_hand)

                # check if the player busted
                if player_value > 21:
                    await ctx.send(f"``You busted! Your hand is worth {player_value}. You lost {bet} chips.``")

                    break
            elif move.content.lower() == "!stand":
                # the player is done taking their turn
                break

        # let the dealer take their turn
        if player_value <= 21:
            await ctx.send(f"``The dealer's HIDDEN CARD was {dealer_hand[1][0]} of {dealer_hand[1][1]}``")
            while dealer_value < 17:
                # draw a card and add it to the dealer's hand
                dealer_hand.append(deck.pop())
                dealer_value = calculate_hand(dealer_hand)

            # show the final hands
            await ctx.send(f"``Your hand: {', '.join(card[0] + ' of ' + card[1] for card in player_hand)}``")
            await ctx.send(f"``Dealer's hand: {', '.join(card[0] + ' of ' + card[1] for card in dealer_hand)}``")

            # determine the winner
            if dealer_value > 21:
                await ctx.send(f"``The dealer busted! You win {bets2} chips!``")
            elif dealer_value == player_value:
                await ctx.send(f"``It's a tie! You get {bet} chips back.``")
            elif dealer_value > player_value:
                await ctx.send("``The dealer wins!``")
            elif dealer_value < player_value and player_value == 21:
                await ctx.send(f"``BLACKJACK! You win {bets} chips!``")
    else:
        await ctx.send("``Invalid bet. Please bet between 1 and 100 chips.``")

def calculate_hand(hand):
    # calculate the value of a hand
    values = {
        "Ace": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 10,
        "Queen": 10,
        "King": 10
        }
    num_aces = sum(card[0] == "Ace" for card in hand)
    value = sum(values[card[0]] for card in hand)
    while num_aces > 0 and value > 21:
        value -= 10
        num_aces -= 1
    return value

@client.command(name='bal', help="Check your Blackjack balance")
async def balance(ctx):
    await bal.balance(ctx)

@client.command(name='leaderboard', help="Check the Blackjack leaderboard")
async def leaderboardy(ctx, client=client):
    await leaderboard.leaderboard(ctx, client)

    # Format the leaderboard
    leaderboard = ''
    for i in range(len(rows)):
        user = client.get_user(rows[i][0])
        leaderboard += f"{i+1}. {user.name} - {rows[i][1]} chips "

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

client.run(os.getenv('token'))