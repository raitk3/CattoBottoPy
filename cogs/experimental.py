"""Experimental things"""

from discord.ext import commands
import asyncio
import logging
from helpers import helpers

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.experimental")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Experimental tools are loaded')

async def setup(bot):
    await bot.add_cog(Experimental(bot))