"""Random AU queue handler"""

from discord.ext import commands
from discord import Embed, ButtonStyle, Interaction
from discord.ui import Button, View, button

import logging

class AmongUsHelpers(commands.Cog, name='AU Helpers'):
    """Among us related things"""
    
    def __init__(self, bot):
        self.bot = bot
        self.current_imp = None
        self.queue = []
        self.logger = logging.getLogger("CattoBotto.AU_Helpers")

    class Buttons(View):
        def __init__(self, au_handler, *, timeout=180):
            super().__init__(timeout=timeout)
            self.logger = logging.getLogger("CattoBotto.buttons")
            self.au_handler = au_handler

        @button(label="Add me", style=ButtonStyle.green, emoji="➕")
        async def add_me(self, interaction: Interaction, button: Button):
            await self.au_handler.add_imp(interaction.channel, interaction.user.name)
            await interaction.message.delete()


        @button(label="Next", style=ButtonStyle.blurple, emoji="➡")
        async def next_imp(self, interaction: Interaction, button: Button):
            self.au_handler.next_imp()
            await self.au_handler.send(interaction.channel, f"Set {self.au_handler.current_imp} as the seeker.")
            await interaction.message.delete()

        @button(label="Clear", style=ButtonStyle.red, emoji="❎")
        async def clear(self, interaction: Interaction, button: Button):
            self.au_handler.clear_imps()
            await self.au_handler.send(interaction.channel, "Cleared the queue")
            await interaction.message.delete()

        @button(label="Discard", style=ButtonStyle.gray, emoji="🗑️")
        async def finish(self, interaction: Interaction, button: Button):
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Among Us tools are loaded")

    @commands.command()
    async def init_au(self, ctx):
        """Get current imp and queue is anyone is waiting"""
        await self.send(ctx)

    @commands.command()
    async def add_imp(self, ctx, *args):
        """Add someone into the seeker queue"""
        for name in args:
            self.queue.append(name)
        await self.send(ctx, f"Added {', '.join(args)} to queue")
        
    def next_imp(self):
        """Set next imp."""
        if len(self.queue) == 0:
            self.current_imp = None
        else:
            self.current_imp = self.queue[0]
            self.queue = self.queue[1:]

    def clear_imps(self):
        """Clear current imp and queue of imps."""
        self.current_imp = None
        self.queue = []

    async def send(self, ctx, status_msg = None):
        embed = Embed(title="AMONG US QUEUE HANDLER")
        if status_msg:
            embed.add_field(name='', value=status_msg, inline=False)
        if self.current_imp is None:
            embed.add_field(name='Current imp:', value="None", inline=False)
        else:
            embed.add_field(name="Current imp:", value = self.current_imp, inline=False)
        if len(self.queue) > 0:
            lines = []
            for i, name in enumerate(self.queue):
                char = "└" if i == len(self.queue) - 1 else "├"
                lines.append(f"{char}─ {name}")
            embed.add_field(name="Queue: ", value = "\n".join(lines), inline=False)
        await ctx.send(embed=embed,
                       view = self.Buttons(self)
                       )

async def setup(bot):
    await bot.add_cog(AmongUsHelpers(bot))