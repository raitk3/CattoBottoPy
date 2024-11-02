"""Experimental things"""

import discord
from discord import interactions
from discord.ext import commands
import asyncio
import logging
from helpers import helpers

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.experimental")
        self.last_sent = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Experimental tools are loaded')
        
    @commands.command()
    async def channel_id(self, ctx):
        print("Hi")
        id = ctx.channel.id
        print(id)
        await ctx.send(id)

    @commands.command()
    async def test(self, ctx):
        print(ctx.author.id)
        await ctx.author.send('<a:assslap:929176697415270491>')


async def setup(bot):
    await bot.add_cog(Experimental(bot))