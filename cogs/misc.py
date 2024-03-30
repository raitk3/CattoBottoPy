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
        id = ctx.author
        self.logger.info(f"Received ping from {id}")
        await ctx.send(f"Pong {id}!")

    @commands.command()
    async def about(self, ctx):
        """Idk, it's something? ¯\_(ツ)_/¯"""
        text = ["```",
                "╔════════════════════════════════════════════════╗",
                "║ Awwh, I didn't know you cared <3               ║",
                "║ Or was it just an accident? :D                 ║",
                "╟────────────────────────────────────────────────╢",
                "║         ▄█                    Made by sBYTEr   ║",
                "║       ▄▀ █                    2021 - 2024      ║",
                "║     ▄▀   █                                     ║",
                "║   ▄▀▄    █    ▄▀▀▄                             ║",
                "║ ▄▀   ▀▄  █  ▄▀    █                            ║",
                "║  ▀▄    ▀▄█▄▀    ▄▀                             ║",
                "║   ▄▀    ▄█▄    ▀▄                              ║",
                "║ ▄▀    ▄▀ █ ▀▄    ▀▄                            ║",
                "║  ▀▄ ▄▀   █   ▀▄  ▄▀                            ║",
                "║    ▀     ▀     ▀▀                              ║",
                "╟────────────────────────────────────────────────╢",
                "║ Github repo:                                   ║",
                "║ https://github.com/raitk3/CattoBottoPy         ║",
                "║ Issues and feature requests can be added here: ║",
                "║ https://github.com/raitk3/CattoBottoPy/issues  ║",
                "╚════════════════════════════════════════════════╝",
                "```"]
        embed = Embed(title="CattoBotto",
                url="https://github.com/raitk3/CattoBottoPy",
                description="\n".join(text))
        await ctx.send(embed=embed)

    @commands.command()
    async def mark_error(self, ctx, message = ""):
        server = ctx.guild.id
        server_name = ctx.guild.name
        "In case bot makes something unexpected, mark error place in logs, so I would know something happened."
        self.logger.error(f"[{server_name} ({server})] Marked error")
        if message:
            self.logger.error(message)
        await ctx.send("Error noted and marked in logs. Thank you!")

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))