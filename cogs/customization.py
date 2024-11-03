"""Customization stuff"""

import discord
from discord import interactions
from discord.ext import commands
import asyncio
import logging
from helpers import helpers

class Customization(commands.Cog, name='Customization'):
    """Change your name colour n'stuff"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.customization")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Customization tools are loaded')

    @commands.command()
    async def namecolor(self, ctx, color: str = commands.parameter(description="- Chosen color name or hex code")):
        """Change your name to your chosen colour.
        
        A new role will be created with your username, which will use the specified color.
        Supported colors are: amber, black, blue, bluegrey, brown, cyan, deeporange, deeppurple, indigo, lime, lightblue, lightgreen, green, grey, magenta, orange, pink, purple, red, rose, teal, yellow

        Additionally a hex code can be used. Hex code must be given Without "0x".
        Useful tool for copying hex codes: https://materialui.co/colors/
        """

        user = ctx.author
        username = user.name

        if helpers.is_username_excluded(username):
            self.logger.warn(f"{username} tried changing color")
            await ctx.send("Sorry, your username is not supported")

        guild = ctx.guild
        color = helpers.get_color(color)
        hex_color = int(f"0x{color}", 16)
        self.logger.info(f"{username} wants to change colour to {hex_color}")
        roles_list = guild.roles
        self.logger.info(f"Roles list: {[role.name for role in roles_list]}")
        role_exists = len([role for role in roles_list if role.name == username]) > 0
        self.logger.info(f"Role already exists: {role_exists}")

        if not role_exists:
            self.logger.info(f"Creating role {username} with color {color}")
            await guild.create_role(name=username, color=discord.Color(hex_color))
            self.logger.info(f"Assigning role to {username}")
        else:
            self.logger.info(f"Changing role {username} color to {color}")
            role = discord.utils.get(ctx.guild.roles, name=username)
            await role.edit(color=discord.Color(hex_color))

        role = discord.utils.get(ctx.guild.roles, name=username)
        await user.add_roles(role)


async def setup(bot):
    await bot.add_cog(Customization(bot))