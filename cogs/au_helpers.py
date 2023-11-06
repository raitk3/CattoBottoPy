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

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Among Us tools are loaded")

    @commands.command()
    async def get_imp(self, ctx):
        """Get current imp and queue is anyone is waiting"""
        await self.send(ctx)

    @commands.command()
    async def add_imp(self, ctx, *args):
        """Add someone into the imp queue"""
        for name in args:
            self.queue.append(name)
        
        await self.send(ctx, f"Added {', '.join(args)} to queue")
        
        
    @commands.command()
    async def next_imp(self, ctx, name=None):
        """Set next imp. When you call next with a name, it will add first into the queue."""
        if name:
            self.queue = [name] + self.queue
            await self.send(ctx, f"Added {name} first into the queue")
        elif len(self.queue) == 0:
            self.current_imp = None
            await self.send(ctx, f"Queue is empty")
        else:
            self.current_imp = self.queue[0]
            self.queue = self.queue[1:]
            await self.send(ctx, f"{self.current_imp} is now the imp")

    @commands.command()
    async def clear_imps(self, ctx):
        """Clear current imp and queue of imps."""
        self.current_imp = None
        self.queue = []
        await self.send(ctx, f"Imp queue is cleared")

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
        await ctx.send(embed=embed
                       #, view = ButtonView(self)
                       )
    
class ButtonView(View):
    def __init__(self, au_helpers: AmongUsHelpers):
        super().__init__()
        self.au_helpers = au_helpers  

    @button(label="Press Me")
    async def press_me(interaction: Interaction, button: Button):
        # I don't remember if it's send or send_message
        await interaction.response.send_message(f"My label is {button.label}")

async def setup(bot):
    await bot.add_cog(AmongUsHelpers(bot))