import pycache_remove
import bot

if __name__ == '__main__':
    pycache_remove.remove_pycache()
    bot.client.run(bot.DISCORD_TOKEN)