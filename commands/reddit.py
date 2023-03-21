import praw
import random
import os
from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                    client_secret=os.getenv('client_secret'),
                    user_agent=os.getenv('user_agent'))

async def meme(ctx, message):
    try:
        subreddit = reddit.subreddit(message)
        all_subs = []
        hot = subreddit.hot(limit=100)

        for submission in hot:
            all_subs.append(submission)

        while True:
            random_sub = random.choice(all_subs)
            all_subs.remove(random_sub)
            if random_sub.stickied:
                continue
            else:
                break

        await ctx.send(f'``{random_sub.title}``\n{random_sub.url}')
    except Exception:
        await ctx.send(f'``Invalid subreddit.``')
        return