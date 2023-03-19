import praw
import random

reddit = praw.Reddit(client_id='Umj3PcYICUCd-F2litkmnw',
                    client_secret='VCIOMQnuko0O3vEdKEBcktS_00yW1g',
                    user_agent='meme:584171:v1.0 (by /u/VaxlyQ)')

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

        await ctx.send(f'```{random_sub.title}```\n{random_sub.url}')
    except Exception:
        await ctx.send(f'```Invalid subreddit.```')
        return