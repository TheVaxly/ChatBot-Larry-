import os
from dotenv import load_dotenv
load_dotenv()
from googleapiclient.discovery import build
import discord
import random

async def subscribers(ctx, user_input):
    try:    
        api_service_name = "youtube"
        api_version = "v3"
        key=os.getenv("key")
        youtube = build(api_service_name, api_version, developerKey=key)
        request = youtube.channels().list(part="statistics", forUsername=user_input)
        response = request.execute()
        subscirbers = response["items"][0]["statistics"]["subscriberCount"]
        await ctx.send(embed=discord.Embed(title=f"{user_input} has {subscirbers} subscribers", color=discord.Color.green()))
    except Exception:
        await ctx.send(embed=discord.Embed(title="Couldn't find subscriber count", description="Try other some channel", color=discord.Color.red()))
        return

def search_youtube(query):
    try:
        api_service_name = "youtube"
        api_version = "v3"
        key=os.getenv("key")
        youtube = build(api_service_name, api_version, developerKey=key)
        request = youtube.search().list(
            part="id",
            q=query,
            type="video"
        )
        response = request.execute()
        if len(response['items']) == 0:
            return
        else:
            video_ids = [item['id']['videoId'] for item in response['items']]
            random_video_id = random.choice(video_ids)
            return f"https://www.youtube.com/watch?v={random_video_id}"
    except Exception:
        return None

async def youtube(ctx, query):
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
    video_url = search_youtube(query)
    if video_url is None:
        await ctx.send(embed=discord.Embed(title="Couldn't find video", description="Try other some video", color=discord.Color.red()))
    else:
        await ctx.send(video_url, view=DeleteButton(timeout=10 * 60))