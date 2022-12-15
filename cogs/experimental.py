from discord import FFmpegPCMAudio, ClientException, opus, DiscordException
from discord.ext import commands
import asyncio
from helpers import helpers, youtube_downloader

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Experimental tools are loaded')

    @commands.command()
    async def join_vc(self, ctx):
        """Join vc."""
        print("AH")
        try:
            channel = ctx.author.voice.channel
            print(f"Trying to connect to: {channel}")
            await channel.connect()
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        except ClientException:
            print("You are already connected to a voice channel.")
        except opus.OpusNotLoaded:
            print("The opus library has not been loaded.")
        except DiscordException as ex:
            print(ex)

    @commands.command()
    async def leave_vc(self, ctx):
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


    @commands.command()
    async def play(self, ctx, url):
        print("PLAY A SONG")
        if url == "test":
            url = "https://youtu.be/doEqUhFiQS4"
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            print(server, voice_channel)

            async with ctx.typing():
                filename = await youtube_downloader.YTDLSource.from_url(url, loop=self.bot.loop)
                print("Playyy")
                voice_channel.play(FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
async def setup(bot):
    await bot.add_cog(Experimental(bot))