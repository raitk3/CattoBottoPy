"""Helper functions for bot"""
import logging
import asyncio

logger = logging.getLogger("CattoBotto.helper")

def is_user(message, user, override):
    if override:
        logger("Purge everyones messages.")
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

async def send_aaaa(ctx):
    logger.debug("Sending AAAAAA")
    await ctx.send("AAAAA")
