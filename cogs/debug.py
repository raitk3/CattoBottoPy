"""Debug methods to test that bot is awake and functions properly"""

import logging
from discord import app_commands
from discord.ext import commands
from helpers import helpers

class Debug(commands.Cog, name='__Debug__'):
    """Debugging"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.debug_enabled = set()
        self.logger = logging.getLogger("CattoBotto.debug")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Debug tools are loaded')

    async def msg(self, ctx, message, override=False):
        server = ctx.guild.id
        server_name = ctx.guild.name
        self.logger.warning(f"[{server_name} ({server})] Sent {message} into a chat")
        if ctx.author in self.debug_enabled or override:
            await ctx.author.send(message)

    @commands.command(hidden=True)
    async def add(self, ctx, left: int, right: int):
        """
        Add two numbers together.
        """
        server = ctx.guild.id
        server_name = ctx.guild.name
        result = left + right
        self.logger.debug(f"[{server_name} ({server})] Did some math: {left} + {right} = {result}")
        await ctx.send(f"{left} + {right} = {result}")

    @commands.command(hidden=True)
    async def junk(self, ctx, number):
        """Send n numbers 5 at a time."""
        server = ctx.guild.id
        server_name = ctx.guild.name
        self.logger.debug(f"[{server_name} ({server})] Sending {number} numbers")
        for i in range(int(number)):
            await self.msg(ctx, i, True)

    @commands.command(hidden=True)
    async def set_debug(self, ctx, value: bool = None):
        """Set debug mode for debuggers."""
        user = ctx.author
        if helpers.is_user_debugger(user):
            if value is None and user not in self.debug_enabled or value:
                self.debug_enabled.add(user)
                await self.msg(ctx, f"Debugger set True for {user}.", True)
            elif (value is None or not value) and user in self.debug_enabled:
                self.debug_enabled.remove(user)
                await self.msg(ctx, f"Debugger set False for {user}.", True)
            else:
                await self.msg(ctx, f"Debugging is already off for {user}.", True)
        else:
            logging.info(f"{user} tried enabling debugging but was not allowed to")
            await self.msg(ctx, "What are you trying to do? You don't have debugging rights.", True)


async def setup(bot):
    await bot.add_cog(Debug(bot))
