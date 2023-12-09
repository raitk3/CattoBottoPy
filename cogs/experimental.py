"""Experimental things"""

import discord
from discord import interactions
from discord.ext import commands
import asyncio
import logging
from helpers import helpers

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
            self.logger = logging.getLogger("CattoBotto.buttons")

        @discord.ui.button(label="Hi", style=discord.ButtonStyle.blurple)
        async def say_hi(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("hi")
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.experimental")

    @commands.command()
    async def button(self, ctx):
        self.logger.debug("Creating view")
        view = self.Buttons()
        self.logger.debug("Sending button embed")
        await ctx.send("HEYO", view = view)
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Experimental tools are loaded')

async def setup(bot):
    await bot.add_cog(Experimental(bot))