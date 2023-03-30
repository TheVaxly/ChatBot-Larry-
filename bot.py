from discord.ext import commands
import discord
import commands.roll as roll, commands.reddit as reddit, commands.ask as ask, commands.game as game
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from commands.responses import send_responses
from googleapiclient.discovery import build
import random

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="rule34"))
    await client.tree.sync()

@client.command(name='ask')
async def ask_command(ctx, *, user_input="Tell me a joke"):
    await ask.ask_command(ctx, user_input=user_input)

@client.command(name='roll')
async def roll_command(ctx, *, dice: str = ''):
    await roll.roll_command(ctx, dice=dice)


@client.command(name='command')
async def help_command(ctx):
    await ctx.send('```Commands:\n!ask [question]\n!roll [xdy]\n!clearbot [amount]\n!clearuser [user] [amount]\n!help```')

@client.command(name="clearall")
async def clear_all(ctx):
    warning_msg = await ctx.send("Are you sure you want to delete all messages in this channel? This action cannot be undone. Type ``!yes`` to confirm.")
    try:
        async def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "!yes"
        await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await warning_msg.delete()
        await ctx.send("Command canceled. You did not confirm within 30 seconds.")
        return
    else:
        await warning_msg.delete()
    await ctx.channel.purge(limit=None)
    await ctx.send(f"``All messages have been deleted.``")

    print(f"{ctx.author.name} deleted all messages.")

@client.command(name='reddit')
async def meme(ctx, message):
    await reddit.meme(ctx, message)

@client.command(name='subs')
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
        await ctx.send("``Please enter a valid move.``")
        return  
    else:
        await game.game(ctx, message)

@client.tree.command(name='blackjack', description="Play blackjack")
@discord.app_commands.describe(bet='How much do you want to bet?(1-100)')
async def blackjack(ctx, bet: int):
        await int.defer(thinking=True)
        bets = bet * 1.5 + bet
        bets = int(bets)
        bets2 = bet + bet
        chips = []
        chips.append(bet)
        player = ctx.author
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
                move = await client.wait_for('message', check=lambda m: m.author == player)

                if move.author != ctx.author:
                    await ctx.send("``Only the player can make a move.``")
                    return
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

client.run(os.getenv('token'))