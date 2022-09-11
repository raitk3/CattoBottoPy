import discord.message
from discord.ext import commands

import debug
import helpers

#token_old = 'OTEzNzkyNjI0MDQ4MDc4ODY4.GEU918.n846Q6FjzLyLdWSI6N2vjRgyTbqhqBQJpeOgO4'
PERMISSIONS = '8'

intents = discord.Intents.default()
intents.message_content = True
description = '''Rait wanted to do a bot, so uhh...here it is!'''
bot = commands.Bot(command_prefix='!', description=description, intents=intents)


"""
COMMANDS
"""

@bot.command()
async def add(ctx, left: int, right: int):
    """Add two numbers together."""
    await ctx.send(f"{left} + {right} = {left+right}")

@bot.command()
async def ping(ctx):
    """Check connection and user detection."""
    id = str(ctx.author)[:-5]
    
    if helpers.is_user_debugger(ctx.author):
        await debug.msg(ctx, f"Pong {id}, you have debugger rights.", True)
    await ctx.send(f"Pong {id}!")

@bot.command()
async def join_music(ctx):
    """Join vc."""
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave_music(ctx):
    """Leave vc."""
    await ctx.voice_client.disconnect()

@bot.command()
async def purge(ctx, number, user=""):
    """Remove messages from chat."""
    if (ctx.author in debug.debug_enabled or helpers.is_user_admin(ctx.author)):
        override = user == ""
        number_of_messages = min(100, int(number))
        await ctx.send(f"Removing messages from {user} from last {number_of_messages} messages")
        channel = ctx.channel
        deleted = await channel.purge(limit=number_of_messages, check=lambda x, u=user, o=override: helpers.is_user(x, u, o))
        await ctx.send(f'Deleted {len(deleted)} message(s)')
    else:
        await ctx.send(f"You're not permitted to purge!")

@bot.command()
async def junk(ctx, number):
    """Send n numbers 5 at a time."""
    for i in range(int(number)):
        await debug.msg(ctx, i, True)

@bot.command()
async def set_debug(ctx, value: bool = None):
    """Set debug mode for debuggers."""
    user = ctx.author
    if helpers.is_user_debugger(user):
        if value is None and user not in debug.debug_enabled or value:
            debug.debug_enabled.add(user)
            await debug.msg(ctx, f"Debugger set True for {user}.", True)
        elif (value is None or not value) and user in debug.debug_enabled:
            debug.debug_enabled.remove(user)
            await debug.msg(ctx, f"Debugger set False for {user}.", True)
        else:
            await debug.msg(ctx, f"Debuging is already off for {user}.", True)   

@bot.command()
async def add_sticker(ctx:commands.Context, name, link=""):
    """Make attatched picture a sticker?"""
    await ctx.send(f"Adding that picture as an emoji :{name}:")
    helpers.save_img(link)
    with open("temp.png", "rb") as img:
        img_byte = img.read()
        await ctx.message.guild.create_custom_emoji(name = (name), image = img_byte)
    await ctx.send("Done")

@bot.command()
async def dodo_mins(ctx:commands.Context, time: float):
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
        message += " ) for us mortals."
    await ctx.send(message , True)

"""
EVENTS
"""

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
    token=""
    with open("token.txt") as f:
        token = f.read()
    bot.run(token)