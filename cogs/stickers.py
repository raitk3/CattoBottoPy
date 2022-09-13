from discord.ext import commands


class Stickers(commands.Cog, name='Sticker'):
    """Add stickers"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sticker tools are loaded')

        
async def setup(bot):
    await bot.add_cog(Stickers(bot))