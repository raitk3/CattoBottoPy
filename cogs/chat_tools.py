"""Misc tools to help with chat related things"""

import logging

from discord.ext import commands
from helpers import helpers

class ChatTools(commands.Cog, name='Chat'):
    """Chat related tools"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.chat_tools")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Chat tools are loaded')

    @commands.command()
    async def purge(self, ctx, number, user=""):
        """Remove messages from chat."""
        debug = self.bot.get_cog('__Debug__')
        author = ctx.author
        channel = ctx.channel
        self.logger.info(f"{ctx.author} tries to purge {number} of messages from {ctx.guild.name}.{channel}{'' if user == '' else f' by {user}'}")
        
        if (author in debug.debug_enabled or helpers.is_user_admin(author)):
            override = user == ""
            number_of_messages = min(100, int(number))
            username = 'everyone' if user == '' else user
            self.logger.info(f"Removing messages by {username} from last {number_of_messages} messages")
            await ctx.send(f"Removing messages by {username} from last {number_of_messages} messages")
            
            deleted = await channel.purge(limit=number_of_messages, check=lambda x, u=user, o=override: helpers.is_user(x, u, o))
            self.logger.info(f'Deleted {len(deleted)} message(s)')
            await ctx.send(f'Deleted {len(deleted)} message(s)')
        else:
            self.logger.error(f"{author} tried purging but debug wasn't enabled or user is not admin.")
            await ctx.send(f"You're not permitted to purge!")
        
async def setup(bot):
    await bot.add_cog(ChatTools(bot))