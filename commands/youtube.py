import os
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
        print(response)
        subscirbers = response["items"][0]["statistics"]["subscriberCount"]
        await ctx.send(f"``{user_input} has {subscirbers} subscribers``")
    except Exception:
        await ctx.send("``No subscribers count found.``")
        return