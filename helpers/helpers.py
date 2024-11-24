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
    debugger = "debug" in [role.name.lower() for role in user.roles]
    logger.debug(f"{user} is{' not' if not debugger else ''} a debugger.")
    return debugger

def is_user_admin(user):
    admin = "cbadmin" in [role.name.lower() for role in user.roles]
    logger.debug(f"{user} is{' not' if not admin else ''} an admin.")
    return admin

def is_username_excluded(username):
    return username.lower in ["cbadmin", "moderator", "debugger", "mod", "dev"]

def get_color(color):
    colors_map = {
        "000000": "010101",
        "amber": "FFC107",
        "black": "010101",
        "blue": "2196F3",
        "bluegrey": "607D8B",
        "brown": "795548",
        "cyan": "4DD0E1",
        "deeporange": "FF5722",
        "deeppurple": "673AB7",
        "indigo": "3F51B5",
        "lime": "CDDC39",
        "lightblue": "03A9F4",
        "lightgreen": "8BC34A",
        "green": "4CAF50",
        "grey": "9E9E9E",
        "magenta": "FF00FF",
        "orange": "FF9800",
        "pink": "EC407A",
        "purple": "9C27B0",
        "red": "F44336",
        "rose": "F48FB1",
        "teal": "009688",
        "yellow": "FFEB3B",
    }
    return colors_map.get(color, color)

async def send_aaaa(ctx):
    logger.debug("Sending AAAAAA")
    await ctx.send("AAAAA")
