"""Helper functions for bot"""
import logging
import asyncio

import colorsys

print()

logger = logging.getLogger("CattoBotto.helper")

def is_user(message, user, override):
    if override:
        return True
    author = str(message.author.id)
    user_strip = user[2:-1]
    logger.debug(f"Message author: {author}, user to purge: {user_strip}")
    return author == user_strip

def is_user_debugger(user):
    debugger = "debug" in [role.name for role in user.roles]
    logger.debug(f"{user} is{' not' if not debugger else ''} a debugger.")
    return debugger

def is_user_admin(user):
    admin = "admin" in [role.name for role in user.roles]
    logger.debug(f"{user} is{' not' if not admin else ''} an admin.")
    return admin

def is_username_excluded(username):
    return username.lower in ["admin", "moderator", "debugger", "mod", "dev"]

def get_color(color):
    colors_map = {
        "000000": "010101",
        "black": "010101",
        "red": "ff0000",
        "green": "00ff00",
        "blue": "0000ff",
        "grey": "777777",
        "gray": "777777",
        "cyan": "00ffff",
        "magenta": "ff00ff",
        "yellow": "ffff00",
        "orange": "ff7700",
    }

    return colors_map.get(color, color)

async def send_aaaa(ctx):
    logger.debug("Sending AAAAAA")
    await ctx.send("AAAAA")
