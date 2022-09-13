"""Helper functions for bot"""
from discord.ext import commands

import urllib


def is_user(message, user, override):
    if override:
        return True
    author = str(message.author.id)
    user_strip = user[2:-1]
    print(f"Message author: {author}, user to purge: {user_strip}")
    return author == user_strip

def is_user_debugger(user):
    return "debug" in [role.name for role in user.roles]

def is_user_admin(user):
    return "admin" in [role.name for role in user.roles]

def save_img(url):
    print("Saving image")
    urllib.request.urlretrieve(url, "temp.png")

def remove_img(url):
    pass