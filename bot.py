import asyncio
import logging
import os
import sys

from datetime import datetime

import discord.message
from discord.ext import commands
from helpers.log_formatter import ColorlessFormatter, ColorfulFormatter

# Make logs directory
try:
    os.scandir("logs")
except FileNotFoundError:
    os.makedirs("logs")

# Global logging setup
logger = logging.getLogger("CattoBotto")

# File Handler
log_start = datetime.now().strftime("%Y%m%d_%H%M%S")
fh = logging.FileHandler(f'./logs/cattobotto_{log_start}.log')
fh.setLevel(logging.DEBUG)

# Console Handler
ch = logging.StreamHandler()

# Formatter
formatter = ColorlessFormatter()
colorformatter = ColorfulFormatter()
fh.setFormatter(formatter)
ch.setFormatter(colorformatter)

logger.addHandler(fh)
logger.addHandler(ch)


def init_bot():
    logger.info("CattoBotto started...")
    PERMISSIONS = '8'
    intents = discord.Intents.default()
    intents.message_content = True
    description = '''Rait wanted to do a bot, so uhh...here it is!'''
    return commands.Bot(command_prefix='!', 
                        description=description,
                        intents=intents,
                        permissions=PERMISSIONS,
                        activity=discord.Game(name="stoobid")
                        )

async def load(bot, dev):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            if cog_name in ['experimental', 'debug'] and not dev:
                continue
            logger.info(f"Loading module {cog_name}")
            await bot.load_extension(f'cogs.{cog_name}')

async def main(arguments):
    dev = False
    for argument in arguments:
        if argument in ["--debug", "--dev"]:
            dev = True
        
    if dev:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    bot = init_bot()

    token=""
    with open("token.txt") as f:
        token = f.read()
    await load(bot, dev)
    await bot.start(token)

if __name__ == '__main__':
    args = sys.argv
    asyncio.run(main(args))
