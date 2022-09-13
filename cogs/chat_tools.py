from discord.ext import commands
from helpers import helpers

class ChatTools(commands.Cog, name='Chat'):
    """Chat related tools"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Chat tools are loaded')

    @commands.command()
    async def purge(self, ctx, number, user=""):
        """Remove messages from chat."""
        debug = self.bot.get_cog('Debug')
        if (ctx.author in debug.debug_enabled or helpers.is_user_admin(ctx.author)):
            override = user == ""
            number_of_messages = min(100, int(number))
            await ctx.send(f"Removing messages from {user} from last {number_of_messages} messages")
            channel = ctx.channel
            deleted = await channel.purge(limit=number_of_messages, check=lambda x, u=user, o=override: helpers.is_user(x, u, o))
            await ctx.send(f'Deleted {len(deleted)} message(s)')
        else:
            await ctx.send(f"You're not permitted to purge!")

        
async def setup(bot):
    await bot.add_cog(ChatTools(bot))