import discord
import sqlite3

conn = sqlite3.connect('db/balances.db')
conn.execute('CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, balance INTEGER NOT NULL DEFAULT 0)')

async def leaderboard(ctx, client):
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
    # Get the balances from the database
    cursor = conn.execute('SELECT user_id, balance FROM balances ORDER BY balance DESC')
    rows = cursor.fetchall()

    # Create the leaderboard embed message
    embed = discord.Embed(title="Blackjack Leaderboard", color=0xff0000)

    for i, row in enumerate(rows):
        user = client.get_user(row[0])
        name = user.name if user else "Unknown User"
        balance = row[1]

        embed.add_field(name=f"{i+1}. {name}", value=f"{balance} chips", inline=False)

    view = DeleteButton(timeout=10 * 60)
    await ctx.send(embed=embed, view=view)