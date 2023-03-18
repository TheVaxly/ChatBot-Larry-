import random
import praw
import discord
from discord.ext import commands


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(
            client_id='Umj3PcYICUCd-F2litkmnw',
            client_secret='VCIOMQnuko0O3vEdKEBcktS_00yW1g',
            user_agent='meme:584171:v1.0 (by /u/VaxlyQ)')

    @commands.command(name='reddit')
    async def meme(self, ctx, message):
        subreddit = self.reddit.subreddit(message)
        all_subs = []
        hot = subreddit.hot(limit=150)

        for submission in hot:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)

        await ctx.send(f'{random_sub.title}\n{random_sub.url}')

def setup(client):
    client.add_cog(Reddit(client))