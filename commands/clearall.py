import discord
import asyncio

async def clear_all(ctx, client):
    try:
        warning_msg = await ctx.send(embed=discord.Embed(title="Are you sure you want to delete all messages in this channel?", description="Type `!yes` to confirm.", color=discord.Color.red()))
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "!yes"
        
        response_msg = await client.wait_for('message', check=check, timeout=30)
        
        if response_msg.content.lower() == "!yes":
            await warning_msg.delete()
            await response_msg.delete()
            await ctx.channel.purge(limit=None)
            await ctx.send(embed=discord.Embed(title="Success", description="``All messages have been deleted.``", color=discord.Color.green()))
            
    except asyncio.TimeoutError:
        await warning_msg.delete()
        await ctx.send(embed=discord.Embed(title="Timed out.", description="``You took too long to respond.``", color=discord.Color.red()))
        return
    except Exception:
        await ctx.send(embed=discord.Embed(title="Permission denied", description="``You don't have permission to use this command.``", color=discord.Color.red()))