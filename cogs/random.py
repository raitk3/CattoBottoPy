from discord.ext import commands

class Random(commands.Cog, name='Random'):
    """Random stuff"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Random tools are loaded')

    @commands.command()
    async def dodo_mins(self, ctx:commands.Context, time: float):
        """Recalculate Dodo minutes for our minutes."""
        if time % 1 == 0:
            time = int(time)
        actual_time = 3 * time
        message = f"{time} minutes for Dodo will be {actual_time} minutes"
        hours = actual_time // 60
        minutes = actual_time % 60
        if hours > 0:
            message += " ("
            if hours == 1:
                message += "1 hour"
            elif hours > 0:
                message += f"{hours} hours"
            
            if minutes == 1:
                message += " and 1 minute"
            elif minutes > 0:
                message += f" and {minutes} minutes"
            message += ") for us mortals."
        await ctx.send(message)

        
async def setup(bot):
    await bot.add_cog(Random(bot))