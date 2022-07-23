import discord
from discord.ext import commands

TOKEN = 'OTEzNzkyNjI0MDQ4MDc4ODY4.GEU918.n846Q6FjzLyLdWSI6N2vjRgyTbqhqBQJpeOgO4'
PERMISSIONS = '1445987360'

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

def is_user(message, user, override):
    if override:
        return True
    author = str(message.author.id)
    user_strip = user[2:-1]
    print(f"Message author: {author}, user to purge: {user_strip}")
    return author == user_strip

@bot.command()
async def purge(ctx, number, user=""):
    override = user == ""
    number_of_messages = min(100, int(number))
    await ctx.send(f"Removing messages from {user} from last {number_of_messages} messages")
    channel = ctx.channel
    deleted = await channel.purge(limit=number_of_messages, check=lambda x, y=user, o=override: is_user(x, y, o))
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command()
async def junk(ctx, number):
    for i in range(int(number)):
        await ctx.send(i)
bot.run(TOKEN)
