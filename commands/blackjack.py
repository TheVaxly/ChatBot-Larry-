import discord
import random
import sqlite3
import asyncio

conn = sqlite3.connect('db/balances.db')

# Create the balances table if it doesn't exist
conn.execute('CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)')

# check if the user has a balance, create one if not
def get_balance(user_id):
    cursor = conn.execute("SELECT balance FROM balances WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        conn.execute("INSERT INTO balances (user_id, balance) VALUES (?, ?)", (user_id, 100))
        conn.commit()
        return 1000
    else:
        return row[0]

# update user balance after a bet is placed
def update_balance(user_id, amount):
    cursor = conn.execute("SELECT balance FROM balances WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    balance = row[0] + amount
    conn.execute("UPDATE balances SET balance=? WHERE user_id=?", (balance, user_id))
    conn.commit()

async def blackjack(ctx, bet: int=0, client=None):
    used_double = False
    current_balance = []
    balance = get_balance(ctx.author.id)
    current_balance.append(balance)
    print(current_balance)
    if bet < 0 or bet > balance or bet == 0:
        await ctx.send(embed=discord.Embed(title="Invalid bet", description=f"Please bet between 1 and {get_balance(ctx.author.id)}", color=0xff0000))
        return
    else:

        player = ctx.author
        list_category_id = []
        category_id = ctx.channel.id
        list_category_id.append(category_id)
        
        # find the category channel
        category_channel = client.get_channel(list_category_id[0])

        # check if a game is already in progress
        threads = category_channel.threads
        for thread in threads:
            if thread.name == f"{player.name} Blackjac":
                await ctx.send(embed=discord.Embed(title="Game in progress", description=f"You already have a game in progress. Please finish that game before starting a new one.", color=0xff0000))
                return

        # create the thread under the category channel
        thread = await category_channel.create_thread(name=f"{player.name} Blackjack", type=discord.ChannelType.public_thread)

        # add the player to the thread if not already joined
        await thread.add_user(player)

        update_balance(player.id, -bet)

            # calculate the amount to be paid out for a blackjack
        blackjack_payout = int(bet * 1.5)
        
            # check if the player has enough money to place the bet
        if bet > 0 and bet <= current_balance[0]:
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

                # check if the player has blackjack
                if player_value == 21:
                    update_balance(player.id, blackjack_payout)
                    embed = discord.Embed(title="Blackjack", color=0x00ff00)
                    embed.add_field(name="Bet", value=f"{bet}", inline=True)
                    embed.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                    embed.add_field(name="Dealer's Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in dealer_hand)} = {dealer_value}", inline=False)
                    embed.add_field(name="Result", value="Blackjack! You win automatically!", inline=False)
                    await thread.send(embed=embed)
                    await asyncio.sleep(10)
                    await thread.delete()
                    return

                # send the initial message to the thread as embed
                embed = discord.Embed(title="Blackjack", color=0xff0000)
                embed.add_field(name="Player", value=f"{player.name}", inline=True)
                embed.add_field(name="Balance", value=f"{get_balance(player.id)}", inline=True)
                embed.add_field(name="Bet", value=f"{bet}", inline=True)
                embed.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                embed.add_field(name="Dealer's Hand", value=f"{dealer_hand[0][0]} of {dealer_hand[0][1]}, HIDDEN CARD", inline=False)
                await thread.send(embed=embed)
                # let the player take their turn
                while True:
                    move = await client.wait_for('message', check=lambda m: m.author == player)

                    if move.author != ctx.author:
                        ctx.send(embed=discord.Embed(title="Invalid move", description=f"You can't make a move in someone else's game.", color=0xff0000))
                        continue
                    
                    if move.content.lower() == "split" and move.channel == thread:
                        # split the hand and draw a card for each
                        if get_balance(player.id) < bet:
                            await thread.send(embed=discord.Embed(title="Insufficient funds", description=f"You don't have enough money to split your bet.", color=0xff0000))
                            continue
                        if len(player_hand) > 2:
                            await thread.send(embed=discord.Embed(title="Invalid move", description=f"You can't split after you've already hit.", color=0xff0000))
                            continue
                        if player_hand[0][0] != player_hand[1][0]:
                            await thread.send(embed=discord.Embed(title="Invalid move", description=f"You can only split if you have two cards of the same rank.", color=0xff0000))
                            continue
                        player_hand = [[player_hand[0]], [player_hand[1]]]
                        player_hand[0].append(deck.pop())
                        player_hand[1].append(deck.pop())
                        player_value = calculate_hand(player_hand)
                        split = discord.Embed(title="Split", color=0xff0000)
                        split.add_field(name="Player", value=f"{player.name}", inline=True)
                        split.add_field(name="Bet", value=f"{bet}", inline=True)
                        split.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand[0])} = {calculate_hand(player_hand[0])} | {', '.join(card[0] + ' of ' + card[1] for card in player_hand[1])} = {calculate_hand(player_hand[1])}", inline=False)
                        split.add_field(name="Dealer's Hand", value=f"{dealer_hand[0][0]} of {dealer_hand[0][1]}, HIDDEN CARD", inline=False)
                        await thread.send(embed=split)


                    if move.content.lower() == "double" and move.channel == thread:
                        # double the bet and draw a card
                        if get_balance(player.id) < bet * 2:
                            await thread.send(embed=discord.Embed(title="Insufficient funds", description=f"You don't have enough money to double your bet.", color=0xff0000))
                            continue
                        if len(player_hand) > 2:
                            await thread.send(embed=discord.Embed(title="Invalid move", description=f"You can't double after you've already hit.", color=0xff0000))
                            continue
                        player_hand.append(deck.pop())
                        player_value = calculate_hand(player_hand)
                        double = discord.Embed(title="Double", color=0xff0000)
                        double.add_field(name="Player", value=f"{player.name}", inline=True)
                        double.add_field(name="Bet", value=f"{bet*2}", inline=True)
                        double.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                        double.add_field(name="Dealer's Hand", value=f"{dealer_hand[0][0]} of {dealer_hand[0][1]}, HIDDEN CARD", inline=False)
                        await thread.send(embed=double)

                        # check if the player busted
                        if player_value > 21:
                            await thread.send(embed=discord.Embed(title="Bust", description=f"You busted with a hand value of {player_value}.", color=0xff0000))
                            update_balance(player.id, -bet)
                            await asyncio.sleep(10)
                            await thread.delete()
                            break
                        else:
                            await thread.send(embed=discord.Embed(title="Hidden card", description=f"The dealer's hidden card was {dealer_hand[1][0]} of {dealer_hand[1][1]}.", color=0xff0000))
                            while dealer_value < 17:
                                # draw a card and add it to the dealer's hand
                                dealer_hand.append(deck.pop())
                                dealer_value = calculate_hand(dealer_hand)

                            # show the final hands
                            final = discord.Embed(title="Final hand", color=0xff0000)
                            final.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                            final.add_field(name="Dealer's Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in dealer_hand)} = {dealer_value}", inline=False)
                            await thread.send(embed=final)

                            # determine the winner
                            if dealer_value > 21:
                                dealer_bust = discord.Embed(title="Dealer bust", description=f"The dealer busted with a hand value of {dealer_value}.", color=0xff0000)
                                dealer_bust.add_field(name="Bet", value=f"You won {bet*2} chips.", inline=False)
                                await thread.send(embed=dealer_bust)
                                update_balance(player.id, 3*bet)
                            elif dealer_value == player_value:
                                tie = discord.Embed(title="Tie", description=f"The dealer and you tied with a hand value of {dealer_value}.", color=0xff0000)
                                tie.add_field(name="Bet", value=f"You got your bet back.", inline=False)
                                await thread.send(embed=tie)
                                update_balance(player.id, bet)
                            elif dealer_value > player_value:
                                dealer_wins = discord.Embed(title="Dealer wins", description=f"The dealer won with a hand value of {dealer_value}." ,color=0xff0000)
                                dealer_wins.add_field(name="Bet", value=f"You lost {bet*2} chips.", inline=False)
                                await thread.send(embed=dealer_wins)
                            elif dealer_value < player_value and player_value == 21:
                                blackjack = discord.Embed(title="Blackjack", description=f"You got blackjack!", color=0xff0000)
                                blackjack.add_field(name="Bet", value=f"You won {1.5*bet*2} chips.", inline=False)
                                await thread.send(embed=blackjack)
                                update_balance(player.id, blackjack_payout + bet * 2)
                            await asyncio.sleep(10)
                            await thread.delete()
                            break
                    # handle the player's move
                    if move.content.lower() == "hit" and move.channel == thread:
                        # draw a card and add it to the player's hand
                        player_hand.append(deck.pop())
                        player_value = calculate_hand(player_hand)
                        hit = discord.Embed(title="Hit", color=0xff0000)
                        hit.add_field(name="Player", value=f"{player.name}", inline=True)
                        hit.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                        hit.add_field(name="Dealer's Hand", value=f"{dealer_hand[0][0]} of {dealer_hand[0][1]}, HIDDEN CARD", inline=False)
                        await thread.send(embed=hit)
                        # check if the player has busted
                        if player_value > 21:
                            await thread.send(embed=discord.Embed(title="Bust", description=f"You busted with a hand value of {player_value}.", color=0xff0000))
                            await asyncio.sleep(10)
                            await thread.delete()
                            break
                    
                    elif move.content.lower() == "surrender" and move.channel == thread:
                        # surrender the game and lose half the bet
                        await thread.send(embed=discord.Embed(title="Surrender", description=f"You surrendered the game and lost half your bet.", color=0xff0000))
                        update_balance(player.id, bet / 2)
                        await asyncio.sleep(10)
                        await thread.delete()
                        break
                    
                    elif move.content.lower() == "stand" and move.channel == thread:
                        break

                # let the dealer take their turn
                if player_value <= 21:
                    await thread.send(embed=discord.Embed(title="Hidden card", description=f"The dealer's hidden card was {dealer_hand[1][0]} of {dealer_hand[1][1]}.", color=0xff0000))
                    while dealer_value < 17:
                        # draw a card and add it to the dealer's hand
                        dealer_hand.append(deck.pop())
                        dealer_value = calculate_hand(dealer_hand)

                    # show the final hands
                    final = discord.Embed(title="Final hand", color=0xff0000)
                    final.add_field(name="Your Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in player_hand)} = {player_value}", inline=False)
                    final.add_field(name="Dealer's Hand", value=f"{', '.join(card[0] + ' of ' + card[1] for card in dealer_hand)} = {dealer_value}", inline=False)
                    await thread.send(embed=final)

                    # determine the winner
                    if dealer_value > 21:
                        dealer_bust = discord.Embed(title="Dealer bust", description=f"The dealer busted with a hand value of {dealer_value}.", color=0xff0000)
                        dealer_bust.add_field(name="Bet", value=f"You won {bet} chips.", inline=False)
                        await thread.send(embed=dealer_bust)
                        update_balance(player.id, 2*bet)
                    elif dealer_value == player_value:
                        tie = discord.Embed(title="Tie", description=f"The dealer and you tied with a hand value of {dealer_value}.", color=0xff0000)
                        tie.add_field(name="Bet", value=f"You got your bet back.", inline=False)
                        await thread.send(embed=tie)
                        update_balance(player.id, bet)
                    elif dealer_value > player_value:
                        dealer_wins = discord.Embed(title="Dealer wins", description=f"The dealer won with a hand value of {dealer_value}." ,color=0xff0000)
                        dealer_wins.add_field(name="Bet", value=f"You lost {bet} chips.", inline=False)
                        await thread.send(embed=dealer_wins)
                    elif dealer_value < player_value and player_value == 21:
                        blackjack = discord.Embed(title="Blackjack", description=f"You got blackjack!", color=0xff0000)
                        blackjack.add_field(name="Bet", value=f"You won {1.5*bet} chips.", inline=False)
                        await thread.send(embed=blackjack)
                        update_balance(player.id, blackjack_payout + bet)
                    await asyncio.sleep(10)
                    await thread.delete()
        else:
                await ctx.send(embed=discord.Embed(title="Error", description=f"I dunno what happened but error?", color=0xff0000))
                return

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