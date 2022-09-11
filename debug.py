from discord.ext import commands

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.debug_enabled = set()

    async def msg(self, ctx, message, override=False):
        print(message)
        if ctx.author in self.debug_enabled or override:
            await ctx.author.send(message)


    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(commands.user.name)
        print(commands.user.id)
        print('------')