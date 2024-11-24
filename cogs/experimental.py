"""Experimental things"""

from discord import app_commands
from discord.ext import commands
import logging
from helpers.emoji import Emoji

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.experimental")
        self.last_sent = None
        self.emoji = Emoji()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Experimental tools are loaded')
        
    @commands.command(hidden=True)
    async def channel_id(self, ctx):
        print("Hi")
        id = ctx.channel.id
        print(id)
        await ctx.send(id)

    @commands.command(hidden=True)
    async def test(self, ctx):
        await ctx.author.send(self.emoji.emoji["ass_slap"])


async def setup(bot):
    await bot.add_cog(Experimental(bot))