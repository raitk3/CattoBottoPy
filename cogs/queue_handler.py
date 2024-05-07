"""Random AU queue handler"""

from discord.ext import commands
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View, button

import logging

class QueueHandler(commands.Cog, name='Queue handler'):
    """A simple queue'ing system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.current_seekers = {}
        self.queues = {}
        self.logger = logging.getLogger("CattoBotto.queue_handler")
        self.current_msgs = {}

    class Buttons(View):
        def __init__(self, queue_handler, *, timeout=180):
            super().__init__(timeout=timeout)
            self.logger = logging.getLogger("CattoBotto.buttons")
            self.queue_handler = queue_handler

        @button(label="Add me", style=ButtonStyle.green, emoji="➕")
        async def add_me(self, interaction: Interaction, button: Button):
            user = interaction.user.name
            server = interaction.guild.id
            server_name = interaction.guild.name
            self.logger.debug(f"{interaction.message.id}")
            self.logger.info(f"[{server_name} ({server})] {user} requested to be in the queue")
            await self.queue_handler.add_to_queue(interaction.channel, user)
            await interaction.response.defer()


        @button(label="Next", style=ButtonStyle.blurple, emoji="➡")
        async def next_in_queue(self, interaction: Interaction, button: Button):
            channel = interaction.channel
            server = interaction.guild.id
            server_name = interaction.guild.name
            self.logger.info(f"[{server_name} ({server})] Next one requested")
            await self.queue_handler.next_in_queue(channel)
            await interaction.response.defer()

        @button(label="Clear", style=ButtonStyle.red, emoji="❎")
        async def clear(self, interaction: Interaction, button: Button):
            server = interaction.guild.id
            server_name = interaction.guild.name
            self.logger.info(f"[{server_name} ({server})] Clearing queue requested")
            await self.queue_handler.clear_queue(interaction.channel)
            await interaction.response.defer()

        @button(label="Discard", style=ButtonStyle.gray, emoji="🗑️")
        async def finish(self, interaction: Interaction, button: Button):
            server = interaction.guild.id
            server_name = interaction.guild.name
            self.logger.info(f"[{server_name} ({server})] Discard queue requested")
            self.queue_handler.current_msgs[interaction.guild.id] = None
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Queue handler is are loaded")

    @commands.command()
    async def init_queue(self, ctx, force=''):
        """Start the queue handler"""
        server = ctx.guild.id
        server_name = ctx.guild.name
        self.logger.info(f"[{server_name} ({server})] Initting helpers")

        if server in self.current_msgs and self.current_msgs[server] != None:
            if force not in ['-f', '--force']:
                self.logger.error(f"[{server_name} ({server})] Server already has an instance.")
                await ctx.send("Unable to init as it is already running. "
                               "Use `init_au -f` or `init_au --force` to forcefully restart, or `resend_au` to preserve current queue.")
                return
            else:
                self.current_msgs[server] = None
                self.logger.info(f"[{server_name} ({server})] Queue handler initialised.")


        self.queues[server] = []
        self.current_seekers[server] = None
        await self.send(ctx)

    @commands.command()
    async def add_to_queue(self, ctx, *args):
        """Add someone into the queue"""
        server = ctx.guild.id
        server_name = ctx.guild.name
        self.logger.info(f"[{server_name} ({server})] Add {', '.join(args)} to queue")
        for name in args:
            self.queues[server].append(name)
        self.logger.info(f"[{server_name} ({server})] Added {', '.join(args)} to queue")
        await self.send(ctx, f"Added {', '.join(args)} to queue")
        
    async def next_in_queue(self, channel):
        """Set next seeker."""
        server = channel.guild.id
        server_name = channel.guild.name
        self.logger.info(f"[{server_name} ({server})] Setting next one from the queue")
        if len(self.queues[server]) == 0:
            self.current_seekers[server] = None
        else:
            self.current_seekers[server] = self.queues[server][0]
            self.queues[server] = self.queues[server][1:]
        await self.send(channel, f"Set {self.current_seekers[server]} as the current.")
        #await self.ping_someone(channel, self.current_seekers[server])

    @commands.command()
    async def remove_from_queue(self, channel, index: int=0):
        """Remove n-th one from the queue"""
        server = channel.guild.id
        server_name = channel.guild.name
        index -= 1
        index = max(0, index)
        queue = self.queues[server]
        self.logger.info(f"[{server_name} ({server})] Removing {index} from queue.")
        if index >= len(queue):
            await self.send(channel, f"No such index in queue.")
        
        removed = queue.pop(index)
        self.queues[server] = queue
        await self.send(channel, f"Removed {removed} from the list.")
    
    async def clear_queue(self, channel):
        """Clear current one and queue."""
        server = channel.guild.id
        server_name = channel.guild.name
        self.logger.info(f"[{server_name} ({server})] Clearing queue.")
        self.current_seekers[server] = None
        self.queues[server] = []
        await self.send(channel, f"Cleared queue.")

    def generate_embed(self, server, status_msg):
        current = self.current_seekers[server]
        queue = self.queues[server]
        embed = Embed(title="QUEUE HANDLER")
        if status_msg:
            embed.add_field(name='', value=status_msg, inline=False)
        if current is None:
            embed.add_field(name='Current:', value="None", inline=False)
        else:
            embed.add_field(name="Current:", value = current, inline=False)
        if len(queue) > 0:
            lines = []
            for i, name in enumerate(queue):
                char = "└" if i == len(queue) - 1 else "├"
                lines.append(f"{char}─{i+1} {name}")
            embed.add_field(name="Queue: ", value = "\n".join(lines), inline=False)
        return embed
    
    @commands.command()
    async def resend_queue(self, ctx):
        """Use it in case original posts message has timed out"""
        server = ctx.guild.id
        server_name = ctx.guild.name
        self.logger.info(f"[{server_name} ({server})] Resending AU message.")
        await self.current_msgs[server].delete()
        self.current_msgs[server] = None
        await self.send(ctx, "Resent the message.")

    async def send(self, ctx, status_msg = None):
        self.logger.debug(self.queues)
        server = ctx.guild.id
        embed = self.generate_embed(server, status_msg)
        if server not in self.current_msgs or self.current_msgs[server] == None:
            self.current_msgs[server] = await ctx.send(embed=embed,
                        view = self.Buttons(self, timeout=None))
        else:
            await self.current_msgs[server].edit(embed=embed)

    async def ping_someone(self, ctx, seeker):
        self.logger.info("Pinging someone")
        await ctx.send(f"<@!sbyter> {seeker}")

async def setup(bot):
    await bot.add_cog(QueueHandler(bot))