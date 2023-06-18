from discord import FFmpegPCMAudio, ClientException, opus, DiscordException
from discord.ext import commands
import asyncio
from helpers import helpers, youtube_downloader
from helpers.errors import VoiceConnectionError
import threading

class Experimental(commands.Cog, name='__Experimental__'):
    """Experimental stuff that most likely won't work"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.vc = None
        self.playing = False
        self.queue = []
        self.thread = threading.Thread(target = self.play_next)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Experimental tools are loaded')

    async def add_to_queue(self, url):
        filename = await youtube_downloader.YTDLSource.from_url(url, loop=self.bot.loop)
        self.queue.append(filename)
        self.playing = True
        

    async def play_next(self):
        voice_client = self.ctx.message.guild.voice_client
        if self.playing and not voice_client.is_playing() and len(self.queue) > 0:
                next_song = self.queue.pop(0)
                self.vc.play(FFmpegPCMAudio(executable="ffmpeg.exe", source=next_song))
                await self.ctx.send(f'**Now playing:** {next_song}')
            
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
        self.ctx = ctx
        if url == "test":
            url = "https://youtu.be/doEqUhFiQS4"
        try :
            server = ctx.message.guild
            self.vc = server.voice_client

            async with ctx.typing():
                self.add_to_queue(url)
            self.play_next()
        except:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command()
    async def pause(self, ctx):
        self.playing = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            self.playing = True
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        self.playing = False
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
async def setup(bot):
    await bot.add_cog(Experimental(bot))