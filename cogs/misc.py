"""Experimental things"""

from discord import Embed
from discord.ext import commands
import asyncio
import logging
import re
from helpers import helpers

class Miscellaneous(commands.Cog, name='Miscellaneous'):
    """Random junk"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.misc")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Miscellaneous tools are loaded')

    @commands.command()
    async def ping(self, ctx):
        """Check connection and user detection."""
        id = ctx.author
        self.logger.info(f"Received ping from {id}")
        await ctx.send(f"Pong {id}!")

    @commands.command()
    async def time_left_to_speak(self, ctx, *, args=None):
        """
        Apply a useful formula provided by Zach Star Himself

        Arguments you can to give:
        t: time someone has spoken in seconds
        q: Questions asked by the other person
        dtc: number of "Damn, That's Crazy"s
        mhm: number of "mhm"s
        tc: number of Time checks
        sn: number of Slow Nods
        de: number of DEEP Exhales
        Values that are not given will be left as 0. Floating point numbers will be rounded to the nearest integer.
        
        Taken from https://www.youtube.com/watch?v=a9Xo7VpelgU
        Applies for last 600 seconds (10 minutes)
        """
        values = {"t":0, "q":0, "dtc":0, "mhm":0, "tc":0, "sn":0, "de":0}
        pattern = re.compile(r"(\w+)=([0-9]*\.*[0-9]*)")
        if args:
            for key, value in pattern.findall(args):
                if key in values:
                    values[key] = value

        T = int(round(float(values["t"])))
        Nqabop = int(round(float(values["q"])))
        Ndtc = int(round(float(values["dtc"])))
        Nmhm = int(round(float(values["mhm"])))
        Ntc = int(round(float(values["tc"])))
        Nsn = int(round(float(values["sn"])))
        Nde = int(round(float(values["de"])))

        values_used = f"Values that were used: t={T}, q={Nqabop}, dtc={Ndtc}, mhm={Nmhm}, tc={Ntc}, sn={Nsn}, de={Nde}\n"
        try:
            self.logger.info(f"(600 - {T} + 200 * {Nqabop})/({Ndtc} + {Nmhm} + ({Ntc} / 3) + ({Nsn} / 2) + (1 + {Nde})**1000000)")
            if Nde > 0:
                result = 0
            else:
                result = max(0, round((600 - T + 200 * Nqabop)/(Ndtc + Nmhm + (Ntc / 3) + (Nsn / 2) + (1+Nde)**1000000), 1))
                self.logger.info(f"Result: {result} seconds")
            if result > 120:
                flavour_text = " before we have to classify sound waves as terrorism."
            elif result > 51:
                flavour_text = " to wrap that shit up."
            elif result > 36:
                flavour_text = " before we classify deaf children as privileged."
            elif result > 0:
                flavour_text = " before I patent the razor Q-Tip."
            else:
                flavour_text = ", so it looks like it's time to make a starfish and go fuck yourself."

            await ctx.send(f"{values_used}You have {result} seconds{flavour_text}")
        except Exception:
            await ctx.send(f"{values_used}Something got fucky, fix the command you used.")

    @commands.command()
    async def about(self, ctx):
        """Idk, it's something? ¯\_(ツ)_/¯"""
        text = ["```",
                "╔════════════════════════════════════════════════╗",
                "║ Awwh, I didn't know you cared <3               ║",
                "║ Or was it just an accident? :D                 ║",
                "╟────────────────────────────────────────────────╢",
                "║         ▄█                    Made by sBYTEr   ║",
                "║       ▄▀ █                    2021 - 2024      ║",
                "║     ▄▀   █                                     ║",
                "║   ▄▀▄    █    ▄▀▀▄                             ║",
                "║ ▄▀   ▀▄  █  ▄▀    █                            ║",
                "║  ▀▄    ▀▄█▄▀    ▄▀                             ║",
                "║   ▄▀    ▄█▄    ▀▄                              ║",
                "║ ▄▀    ▄▀ █ ▀▄    ▀▄                            ║",
                "║  ▀▄ ▄▀   █   ▀▄  ▄▀                            ║",
                "║    ▀     ▀     ▀▀                              ║",
                "╟────────────────────────────────────────────────╢",
                "║ Github repo:                                   ║",
                "║ https://github.com/raitk3/CattoBottoPy         ║",
                "║ Issues and feature requests can be added here: ║",
                "║ https://github.com/raitk3/CattoBottoPy/issues  ║",
                "╚════════════════════════════════════════════════╝",
                "```"]
        embed = Embed(title="CattoBotto",
                url="https://github.com/raitk3/CattoBottoPy",
                description="\n".join(text))
        await ctx.send(embed=embed)

    @commands.command()
    async def mark_error(self, ctx, message = ""):
        server = ctx.guild.id
        server_name = ctx.guild.name
        "In case bot makes something unexpected, mark error place in logs, so I would know something happened."
        self.logger.error(f"[{server_name} ({server})] Marked error")
        if message:
            self.logger.error(message)
        await ctx.send("Error noted and marked in logs. Thank you!")

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))