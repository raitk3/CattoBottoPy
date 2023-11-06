"""Experimental things"""

from discord import Embed
from discord.ext import commands
import asyncio
import logging
from helpers import helpers

class Miscellaneous(commands.Cog, name='Miscellaneous'):
    """Random junk"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.misc")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Miscellaneous tools are loaded')

    @commands.command()
    async def ping(self, ctx):
        """Check connection and user detection."""
        id = "".join(str(ctx.author).split("#")[:-1])
        self.logger.info(f"Received ping from {id}")
        await ctx.send(f"Pong {id}!")

    @commands.command()
    async def about(self, ctx):
        text = ["```",
                "╔════════════════════════════════════════╗",
                "║ CattoBotto                             ║",
                "╠════════════════════════════════════════╣",
                "║ Awwh, I didn't know you cared <3       ║",
                "║ Or was it just an accident? :D         ║",
                "╟────────────────────────────────────────╢",
                "║         ▄█            Made by sBYTEr   ║",
                "║       ▄▀ █            2023             ║",
                "║     ▄▀   █                             ║",
                "║   ▄▀▄    █    ▄▀▀▀▄                    ║",
                "║ ▄▀   ▀▄  █  ▄▀     █                   ║",
                "║  ▀▄    ▀▄█▄▀     ▄▀                    ║",
                "║   ▄▀    ▄█▄     ▀▄                     ║",
                "║ ▄▀    ▄▀ █ ▀▄     ▀▄                   ║",
                "║  ▀▄ ▄▀   █   ▀▄   ▄▀                   ║",
                "║    ▀     ▀     ▀▀▀                     ║",
                "╟────────────────────────────────────────╢",
                "║ Github repo:                           ║",
                "║ https://github.com/raitk3/CattoBottoPy ║",
                "╚════════════════════════════════════════╝",
                "```"]
        embed = Embed(title="CattoBottoPy",
                url="https://github.com/raitk3/CattoBottoPy",
                description="\n".join(text))
        await ctx.send("\n".join(text))

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))