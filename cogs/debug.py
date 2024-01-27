"""Debug methods to test that bot is awake and functions properly"""

import logging
from discord.ext import commands
from helpers import helpers

class Debug(commands.Cog, name='__Debug__'):
    """Debugging"""
    def __init__(self, bot):
        self.bot = bot
        self.debug_enabled = set()
        self.logger = logging.getLogger("CattoBotto.debug")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Debug tools are loaded')

    async def msg(self, ctx, message, override=False):
        self.logger.warning(f"Sent {message} into a chat")
        if ctx.author in self.debug_enabled or override:
            await ctx.author.send(message)

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """
        Add two numbers together.
        """
        result = left + right
        self.logger.debug(f"Did some math: {left} + {right} = {result}")
        await ctx.send(f"{left} + {right} = {result}")

    @commands.command()
    async def junk(self, ctx, number):
        """Send n numbers 5 at a time."""
        self.logger.debug(f"Sending {number} numbers")
        for i in range(int(number)):
            await self.msg(ctx, i, True)

    @commands.command()
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

    @commands.command()
    async def mark_error(self, ctx, message = ""):
        "In case bot makes something unexpected, mark error place in logs, so I would know something happened."
        self.logger.error("Marked error")
        if message:
            self.logger.error(message)
        await ctx.send("Error noted and marked in logs. Thank you!")

async def setup(bot):
    await bot.add_cog(Debug(bot))
