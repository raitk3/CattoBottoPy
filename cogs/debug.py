from discord.ext import commands
from helpers import helpers

class Debug(commands.Cog, name='Debug'):
    """Debugging"""
    def __init__(self, bot):
        self.bot = bot
        self.debug_enabled = set()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Debug tools are loaded')

    async def msg(self, ctx, message, override=False):
        self.bot.logger.warning(message)
        if ctx.author in self.debug_enabled or override:
            await ctx.author.send(message)

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Add two numbers together."""
        await ctx.send(f"{left} + {right} = {left+right}")

    @commands.command()
    async def junk(self, ctx, number):
        """Send n numbers 5 at a time."""
        for i in range(int(number)):
            await self.msg(ctx, i, True)

    @commands.command()
    async def ping(self, ctx):
        """Check connection and user detection."""
        id = str(ctx.author)[:-5]
        
        # if helpers.is_user_debugger(ctx.author):
        #    await self.msg(ctx, f"Pong {id}, you have debugger rights.", True)
        await ctx.send(f"Pong {id}!")

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
                await self.msg(ctx, f"Debuging is already off for {user}.", True)


async def setup(bot):
    await bot.add_cog(Debug(bot))
