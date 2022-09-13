from discord.ext import commands

class VC_tools(commands.Cog, name='VC'):
    """VC related stuff"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('VC tools are loaded')

        
async def setup(bot):
    await bot.add_cog(VC_tools(bot))