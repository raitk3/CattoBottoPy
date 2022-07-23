import discord
from discord.ext import commands

import debug
import helpers

TOKEN = 'OTEzNzkyNjI0MDQ4MDc4ODY4.GEU918.n846Q6FjzLyLdWSI6N2vjRgyTbqhqBQJpeOgO4'
PERMISSIONS = '8'

description = '''Rait wanted to do a bot, so uhh...here it is!'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await debug.msg(ctx, f"{left} + {right} = {left+right}", True)

@bot.command()
async def ping(ctx):
    """Check connection and user detection."""
    id = str(ctx.author)[:-5]
    
    if helpers.is_user_debugger(ctx.author):
        await debug.msg(ctx, f"Pong {id}, you have debugger rights.", True)
    else:
        await debug.msg(ctx, f"Pong {id}.!", True)

@bot.command()
async def join_music(ctx):
    """Joins vc"""
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave_music(ctx):
    """Leaves vc"""
    await ctx.voice_client.disconnect()

@bot.command()
async def purge(ctx, number, user=""):
    """Removes messages from chat"""
    override = user == ""
    number_of_messages = min(100, int(number))
    await debug.msg(ctx, f"Removing messages from {user} from last {number_of_messages} messages")
    channel = ctx.channel
    deleted = await channel.purge(limit=number_of_messages, check=lambda x, u=user, o=override: helpers.is_user(x, u, o))
    await debug.msg(ctx, f'Deleted {len(deleted)} message(s)', True)

@bot.command()
async def junk(ctx, number):
    for i in range(int(number)):
        await debug.msg(ctx, i, True)

@bot.command()
async def set_debug(ctx, value: bool = None):
    if helpers.is_user_debugger(ctx.author):
        if value is None:
            debug.debug_enabled = not debug.debug_enabled
        else:
            debug.debug_enabled = value
        await debug.msg(ctx, f"Debugger set to {debug.debug_enabled}.", True)

@bot.command()
async def add_sticker(ctx:commands.Context, name, link=""):
    await debug.msg(ctx, f"Adding that picture as an emoji :{name}:", True)
    helpers.save_img(link)
    with open("temp.png", "rb") as img:
        img_byte = img.read()
        await ctx.message.guild.create_custom_emoji(name = (name), image = img_byte)
    await debug.msg(ctx, "Done")
if __name__ == '__main__':
    bot.run(TOKEN)
