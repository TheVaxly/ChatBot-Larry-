import praw
import random
import os
from dotenv import load_dotenv
load_dotenv()
import discord

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                    client_secret=os.getenv('client_secret'),
                    user_agent=os.getenv('user_agent'))


async def meme(ctx, message):
    class DeleteButton(discord.ui.View):
        async def on_timeout(self):
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=self)
        @discord.ui.button(label="Delete",style=discord.ButtonStyle.danger,custom_id=f"delete_{ctx.message.id}")
        async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
            if button.custom_id == f"delete_{ctx.message.id}":
                await interaction.response.defer()
                await interaction.message.delete()
                self.stop()

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
        view = DeleteButton(timeout=10 * 60)
        
        embed = discord.Embed(title=random_sub.title, url=random_sub.url, color=discord.Color.gold())
        embed.set_image(url=random_sub.url)
        embed.set_footer(text=f"👍 {random_sub.score} | 💬 {random_sub.num_comments}")
        await ctx.send(embed=embed, view=view)
    except Exception as e:
        print(f'Error: {e}')
        await ctx.send(embed=discord.Embed(title="Invalid subreddit.", description="Please enter a valid subreddit.", color=discord.Color.red()))
        return