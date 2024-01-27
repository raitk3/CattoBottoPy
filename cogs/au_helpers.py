"""Random AU queue handler"""

from discord.ext import commands
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View, button

import logging

class AmongUsHelpers(commands.Cog, name='AU Helpers'):
    """Among us related things"""
    
    def __init__(self, bot):
        self.bot = bot
        self.current_seekers = {}
        self.queues = {}
        self.logger = logging.getLogger("CattoBotto.AU_Helpers")
        self.current_msgs = {}

    class Buttons(View):
        def __init__(self, au_handler, *, timeout=180):
            super().__init__(timeout=timeout)
            self.logger = logging.getLogger("CattoBotto.buttons")
            self.au_handler = au_handler

        @button(label="Add me", style=ButtonStyle.green, emoji="➕")
        async def add_me(self, interaction: Interaction, button: Button):
            user = interaction.user.name
            self.logger.info(f"{user} requested to be in the seekers queue")
            await self.au_handler.add_seeker(interaction.channel, user)
            await interaction.response.defer()


        @button(label="Next", style=ButtonStyle.blurple, emoji="➡")
        async def next_seeker(self, interaction: Interaction, button: Button):
            channel = interaction.channel
            await self.au_handler.next_seeker(channel)
            await interaction.response.defer()

        @button(label="Clear", style=ButtonStyle.red, emoji="❎")
        async def clear(self, interaction: Interaction, button: Button):
            await self.au_handler.clear_seekers(interaction.channel)
            await interaction.response.defer()

        @button(label="Discard", style=ButtonStyle.gray, emoji="🗑️")
        async def finish(self, interaction: Interaction, button: Button):
            self.logger.info(f"Discard {interaction.guild.id}")
            self.au_handler.current_msgs[interaction.guild.id] = None
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Among Us tools are loaded")

    @commands.command()
    async def init_au(self, ctx, force=''):
        """Get current imp and queue is anyone is waiting"""
        server = ctx.guild.id
        self.logger.info(f"Initting AU helpers for {server}")

        if server in self.current_msgs and self.current_msgs[server] != None:
            if force not in ['-f', '--force']:
                self.logger.error(f"Server {server} already has an instance.")
                await ctx.send("Unable to init as it is already running. "
                               "Use `init_au -f` or `init_au --force` to forcefully restart, or `resend_au` to preserve current queue.")
                return
            else:
                self.current_msgs[server] = None
                self.logger.info(f"AU helpers for {server} init.")


        self.queues[server] = []
        self.current_seekers[server] = None
        await self.send(ctx)

    @commands.command()
    async def add_seeker(self, ctx, *args):
        """Add someone into the seeker queue"""
        server = ctx.guild.id
        for name in args:
            self.queues[server].append(name)
        self.logger.info(f"Added {', '.join(args)} to {server} queue")
        await self.send(ctx, f"Added {', '.join(args)} to queue")
        
    async def next_seeker(self, channel):
        """Set next imp."""
        server = channel.guild.id
        if len(self.queues[server]) == 0:
            self.current_seekers[server] = None
        else:
            self.current_seekers[server] = self.queues[server][0]
            self.queues[server] = self.queues[server][1:]
        await self.send(channel, f"Set {self.current_seekers[server]} as the seeker.")

    @commands.command()
    async def remove_seeker(self, channel, index: int=0):
        """Remove imp."""
        server = channel.guild.id
        index -= 1
        index = max(0, index)
        seekers_list = self.queues[server]
        self.logger.info(f"Removing {index} from {server} queue.")
        if index >= len(seekers_list):
            await self.send(channel, f"No such index in queue.")
        
        removed = seekers_list.pop(index)
        self.queues[server] = seekers_list
        await self.send(channel, f"Removed {removed} from the list.")
    
    async def clear_seekers(self, channel):
        """Clear current seeker and queue of seekers."""
        server = channel.guild.id
        self.current_seekers[server] = None
        self.queues[server] = []
        await self.send(channel, f"Cleared seekers queue.")

    def generate_embed(self, server, status_msg):
        current_imp = self.current_seekers[server]
        queue = self.queues[server]
        embed = Embed(title="AMONG US QUEUE HANDLER")
        if status_msg:
            embed.add_field(name='', value=status_msg, inline=False)
        if current_imp is None:
            embed.add_field(name='Current imp:', value="None", inline=False)
        else:
            embed.add_field(name="Current imp:", value = current_imp, inline=False)
        if len(queue) > 0:
            lines = []
            for i, name in enumerate(queue):
                char = "└" if i == len(queue) - 1 else "├"
                lines.append(f"{char}─{i+1} {name}")
            embed.add_field(name="Queue: ", value = "\n".join(lines), inline=False)
        return embed
    
    @commands.command()
    async def resend_au(self, ctx):
        server = ctx.guild.id
        await self.current_msgs[server].delete()
        self.current_msgs[server] = None
        await self.send(ctx, "Resent the message.")

    async def send(self, ctx, status_msg = None):
        server = ctx.guild.id
        embed = self.generate_embed(server, status_msg)
        if server not in self.current_msgs or self.current_msgs[server] == None:
            self.current_msgs[server] = await ctx.send(embed=embed,
                        view = self.Buttons(self, timeout=None))
        else:
            await self.current_msgs[server].edit(embed=embed)

async def setup(bot):
    await bot.add_cog(AmongUsHelpers(bot))