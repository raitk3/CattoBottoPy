"""Experimental things"""

from discord import Embed, app_commands
from discord.ext import commands
import logging

class Miscellaneous(commands.Cog, name='Miscellaneous'):
    """Random junk"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.misc")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Miscellaneous tools are loaded')

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx):
        """Check connection and user detection."""
        id = ctx.author
        self.logger.info(f"Received ping from {id}")
        await ctx.send(f"Pong {id}!", ephemeral=True)

    @commands.hybrid_command(name = "time_left_to_speak")
    @app_commands.describe(time_spoken = "Time you have spoken in seconds")
    @app_commands.describe(questions_asked = "Number of questions asked by the other person")
    @app_commands.describe(damn_thats_crazys = "Number of \"damn, that's crazy\"s")
    @app_commands.describe(mhms = "Number of 'mhm's")
    @app_commands.describe(time_checks = "Number of time checks")
    @app_commands.describe(slow_nods = "Number of slow nods")
    @app_commands.describe(deep_exhales = "Number of DEEP EXHALES")
    @app_commands.describe(user = "User who you want to tell this to")
    async def time_left_to_speak(self, ctx,
                                 time_spoken:int=0,
                                 questions_asked:int=0,
                                 damn_thats_crazys:int=0,
                                 mhms:int=0,
                                 time_checks:int=0,
                                 slow_nods:int=0,
                                 deep_exhales:int=0,
                                 user:str=""):
        """
        Apply a useful formula provided by Zach Star Himself

        Values that are not given will be left as 0. Values have to be integers.
        
        Taken from https://www.youtube.com/watch?v=a9Xo7VpelgU
        Applies for last 600 seconds (10 minutes)
        """
        user_text = "You"
        if user != "":
            user_text = f"{user}, you"

        try:
            self.logger.info(f"(600 - {time_spoken} + 200 * {questions_asked})/({damn_thats_crazys} + {mhms} + ({time_checks} / 3) + ({slow_nods} / 2) + (1 + {deep_exhales})**1000000)")
            if deep_exhales > 0:
                result = 0
            else:
                result = max(0, round((600 - time_spoken + 200 * questions_asked)/(damn_thats_crazys + mhms + (time_checks / 3) + (slow_nods / 2) + (1+deep_exhales)**1000000), 1))
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

            await ctx.send(f"{user_text} have {result} seconds{flavour_text}")
        except Exception:
            await ctx.send(f"Something got fucky, fix the command you used.")

    @commands.hybrid_command()
    async def about(self, ctx):
        """Idk, it's something? ¯\_(ツ)_/¯"""
        text = ["```",
                "╔════════════════════════════════════════════════╗",
                "║ Awwh, I didn't know you cared <3               ║",
                "║ Or was it just an accident? :D                 ║",
                "╟────────────────────────────────────────────────╢",
                "║         ▄█                      Made by sBYTEr ║",
                "║       ▄▀ █                         2021 - 2024 ║",
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
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    @app_commands.describe(message = "Error message for me")
    async def mark_error(self, ctx, message:str = ""):
        """
        Mark an error of this bot in logs
        """
        server = ctx.guild.id
        server_name = ctx.guild.name
        "In case bot makes something unexpected, mark error place in logs, so I would know something happened."
        self.logger.error(f"[{server_name} ({server})] Marked error")
        if message:
            self.logger.error(message)
        await ctx.response.send_message("Error noted and marked in logs. Thank you!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))