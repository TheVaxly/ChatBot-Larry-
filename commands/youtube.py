import os
import discord
from dotenv import load_dotenv
load_dotenv()
from googleapiclient.discovery import build

async def subscribers(ctx, *, user_input):
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
        await ctx.send(embed=discord.Embed(title="Subscriber count not available", description="Try other channel", color=discord.Color.red()))
        return