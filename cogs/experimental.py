from discord.ext import commands
from helpers import helpers

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Experimental tools are loaded')

    @commands.command()
    async def join_music(self, ctx):
        """Join vc."""
        print("AH")
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave_music(self, ctx):
        """Leave vc."""
        await ctx.voice_client.disconnect()

    @commands.command()
    async def add_sticker(self, ctx:commands.Context, name, link=""):
        """Make attatched picture a sticker?"""
        await ctx.send(f"Adding that picture as an emoji :{name}:")
        helpers.save_img(link)
        with open("temp.png", "rb") as img:
            img_byte = img.read()
            await ctx.message.guild.create_custom_emoji(name = (name), image = img_byte)
        await ctx.send("Done")

        
async def setup(bot):
    await bot.add_cog(Experimental(bot))