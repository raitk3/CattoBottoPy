import discord
from discord.ext import commands

TOKEN = 'OTEzNzkyNjI0MDQ4MDc4ODY4.YaDpsw.KiosXTUVjh_xcRVEXyk6zXQqK5M'

description = '''Rait wanted to do a bot, so uhh...here it is!'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def test(ctx):
    """Returns info about the sender."""
    id = str(ctx.author)[:-5]
    await ctx.send(id)

@bot.command()
async def join_music(ctx):
    """Joins vc"""
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave_music(ctx):
    """Leaves vc"""
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
