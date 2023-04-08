import commands.responses as responses
import discord

symbol = "```"

async def ask_command(ctx, *, user_input):
    class new(discord.ui.View):
        async def on_timeout(self):
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=self)
        @discord.ui.button(label="New Response", style=discord.ButtonStyle.success, emoji="😏", custom_id=f"new_{ctx.message.id}")
        async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
            if button.custom_id == f"new_{ctx.message.id}" and interaction.user.id == ctx.author.id:
                embeds=discord.Embed(title="Question: " + user_input, description=symbol + responses.send_responses(user_input) + symbol, color=discord.Color.green())
                embeds.set_footer(text="Asked by " + user_name)
                await interaction.response.edit_message(embed=embeds, view=new())
                await interaction.response.defer()
                self.stop()

    try:
        user_name = ctx.author.name

        bot_response = responses.send_responses(user_input)

        embed=discord.Embed(title=f"Question: {user_input}", description=f"{symbol}{bot_response}{symbol}", color=discord.Color.green())
        embed.set_footer(text=f"Asked by {user_name}")
        await ctx.send(embed=embed, view=new(timeout=10 * 60))
    except:
        await ctx.send(embed=discord.Embed(title="Error", description="Something went wrong. Please try again.", color=discord.Color.red()))

async def img(ctx, *, user_input):
    response = responses.generate_image(user_input)
    await ctx.send(response)