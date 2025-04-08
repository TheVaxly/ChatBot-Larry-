import os
from dotenv import load_dotenv
import discord
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse

load_dotenv()

async def subscribers(ctx, user_input):
    await ctx.send(embed=discord.Embed(
        title="Subscriber Count Unavailable",
        description="This feature requires a YouTube API key. Please contact the bot administrator to set this up.",
        color=discord.Color.red()
    ))

def search_youtube(query):
    try:
        # URL encode the search query
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all video links
        video_links = []
        
        # Look for video links in the page source
        for script in soup.find_all('script'):
            script_content = str(script)
            if 'ytInitialData' in script_content:
                # Extract video IDs from the script content
                start_idx = script_content.find('videoId":"')
                while start_idx != -1:
                    start_idx += 10  # Skip 'videoId":"'
                    end_idx = script_content.find('"', start_idx)
                    if end_idx != -1:
                        video_id = script_content[start_idx:end_idx]
                        if len(video_id) == 11:  # YouTube video IDs are 11 characters
                            video_links.append(f"https://www.youtube.com/watch?v={video_id}")
                    start_idx = script_content.find('videoId":"', end_idx)
        
        # Remove duplicates while preserving order
        video_links = list(dict.fromkeys(video_links))
        
        if video_links:
            return random.choice(video_links)
        return None
    except Exception as e:
        print(f"Error searching YouTube: {e}")
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
        await ctx.send(embed=discord.Embed(title="Couldn't find video", description="Try another search term", color=discord.Color.red()))
    else:
        await ctx.send(video_url, view=DeleteButton(timeout=10 * 60))