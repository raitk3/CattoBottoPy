import asyncio
import os

import discord.message
from discord.ext import commands

def init_bot():
    PERMISSIONS = '8'
    intents = discord.Intents.default()
    intents.message_content = True
    description = '''Rait wanted to do a bot, so uhh...here it is!'''
    return commands.Bot(command_prefix='!', description=description, intents=intents, permissions=PERMISSIONS)

async def load(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    bot = init_bot()
    token=""
    with open("token.txt") as f:
        token = f.read()
    await load(bot)
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
