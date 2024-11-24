"""Experimental things"""

from discord import app_commands, ButtonStyle, Interaction
from discord.ext import commands
import logging
import asyncio
from discord.ui import Button, View, button
from helpers.errors import *
from cogs.competition.participant import ParticipantDoesntExistException, ParticipantExistsException
from helpers.emoji import Emoji

from cogs.competition.competitions import *

class CompetitionHandler(commands.Cog, name='Competitions'):
    """
    Competition-leaderboard thing
    
    Creation command can be used in a channel.
    This will create a thread.
    All further commands MUST be used in that thread. 
    """
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("CattoBotto.competition")
        self.competitions = {}
        self.emoji = Emoji()

    class Buttons(View):
        def __init__(self, competition_handler, *, timeout=180):
            super().__init__(timeout=timeout)
            self.logger = logging.getLogger("CattoBotto.buttons")
            self.competition_handler = competition_handler

        @button(label="Join", style=ButtonStyle.green, emoji="➕")
        async def add_me(self, interaction: Interaction, button: Button):
            author = f"<@{interaction.user.id}>"
            self.logger.info(f"{interaction.user} requested to be in a competititon from {interaction.message.id}.")
            try:
                await self.competition_handler.add_participant_from_message(interaction.message.id, author)
            except Exception:
                pass
            await interaction.response.defer()

        # @button(label='Add a result', style=ButtonStyle.blurple, emoji="🆚")
        # async def add_result(self, interaction: Interaction, button: Button):
        #     await interaction.response.defer()

        @button(label="Finish", style=ButtonStyle.gray, emoji="🏁")
        async def end(self, interaction: Interaction, button: Button):
            try:
                await self.competition_handler.end_from_message(interaction.message.id, interaction.user)
            except Exception:
                pass
            await interaction.response.defer()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Competition tools are loaded')

    @commands.hybrid_command()
    @app_commands.describe(title = "Title for the competition")
    async def competition(self, ctx, title="Generic competition"):
        """
        Start a league.

        Start a competition in a league format.
        By default win is worth 3 points, draw 1 point, and defeat 0 points.
        Amount of points awarded can be changed via commands.
        """
        self.logger.info(f"Starting a competition...")
        competition_message = await ctx.send(f"{self.emoji.emoji.get('cat_loading', '')}Initialising competition")
        competition_thread = await competition_message.create_thread(name=title)
        competition = Generic(title, competition_message, competition_thread, buttons=self.Buttons(self, timeout=None))
        competition.set_host(self.convert_to_tag(ctx.author))
        self.competitions[competition_thread.id] = competition
        await self.update_message(competition.thread.id)
        await competition_thread.send("Competition initalisation was successful")
        self.logger.info(f"Competition initialisation in thread {competition.thread.id} was successful.")
        await ctx.message.delete()

    @commands.hybrid_command()
    @app_commands.describe(title = "Title for the league")
    async def league(self, ctx, title="League"):
        """
        Start a league.

        Start a competition in a league format.
        By default win is worth 3 points, draw 1 point, and defeat 0 points.
        Amount of points awarded can be changed via commands.
        """
        self.logger.info(f"Starting a competition...")
        competition_message = await ctx.send(f"{self.emoji.emoji.get('cat_loading', '')}Initialising competition")
        competition_thread = await competition_message.create_thread(name=title)
        competition = League(title, competition_message, competition_thread, buttons=self.Buttons(self, timeout=None))
        competition.set_host(self.convert_to_tag(ctx.author))
        self.competitions[competition_thread.id] = competition
        await self.update_message(competition.thread.id)
        await competition_thread.send("League initalisation was successful")
        self.logger.info(f"League initialisation in thread {competition.thread.id} was successful.")
        await ctx.message.delete()

    @commands.hybrid_command()
    @app_commands.describe(participant = "Participant you'd like to add.")
    async def participant(self, ctx, participant):
        """
        Add a participant to the competition.

        Command can only be used by the moderators and the host.
        For others, joining can be done by the button.
        This command must be used in a thread that the competition is run in.
        """
        self.logger.info(f"Trying to add a participant to a competition")
        try:
            self.logger.info(f"Adding {participant} to the competition")
            thread_id = ctx.channel.id
            competition = self.competitions[thread_id]
            
            competition.add_participant(self.convert_to_tag(ctx.author), participant)
            await self.update_message(ctx.channel.id)
            await ctx.send(f"{participant} added to competition.")
        except ParticipantExistsException as e:
            await e.send_message(ctx)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    @app_commands.describe(points = "Points awarded for victory")
    async def set_win(self, ctx, points:int):
        """
        (League) Set points for match victory as an integer.

        Command can only be used by the moderators and the host.
        """
        
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting win points for {ctx.channel.id}: {points}")
            competition.set_win(self.convert_to_tag(ctx.author), points)
            self.logger.info(f"Setting win points was succesful")
            await ctx.send(f"Match win points is set to {points}", ephemeral=True)
            await self.update_message(ctx.channel.id)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    @app_commands.describe(points = "Points awarded for draw")
    async def set_draw(self, ctx, points:int):
        """
        (League) Set points for match draw as an integer.

        Command can only be used by the moderators and the host.
        """
        
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting draw points for {ctx.channel.id}: {points}")
            competition.set_draw(self.convert_to_tag(ctx.author), points)
            self.logger.info(f"Setting draw points was succesful")
            await ctx.send(f"Match draw points is set to {points}", ephemeral=True)
            await self.update_message(ctx.channel.id)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    @app_commands.describe(points = "Points awarded for defeat")
    async def set_defeat(self, ctx, points:int):
        """
        (League) Set points for match defeat as an integer.

        Command can only be used by the moderators and the host.
        """
        
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting defeat points for {ctx.channel.id}: {points}")
            competition.set_win(self.convert_to_tag(ctx.author), points)
            self.logger.info(f"Setting defeat points was succesful")
            await ctx.send(f"Match win points is set to {points}", ephemeral=True)
            await self.update_message(ctx.channel.id)
        except NotAModException as e:
            await e.send_message(ctx)
    
    @commands.hybrid_command()
    @app_commands.describe(count = "How many rounds is there per game")
    async def set_best_of(self, ctx, count:int):
        """
        (League) Set the number of rounds per game.

        Command can only be used by the moderators and the host.
        """
        
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting best of count for {ctx.channel.id}: {count}")
            competition.set_best_of(self.convert_to_tag(ctx.author), count)
            self.logger.info(f"Setting defeat points was succesful")
            await ctx.send(f"Match number of rounds is set to {count}", ephemeral=True)
            await self.update_message(ctx.channel.id)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    async def reload(self, ctx):
        """
        Use this in case buttons time out for whatever reason.

        Command can be used by anyone.
        """
        await self.update_message(ctx.channel.id)
        await ctx.send("Reloaded the main message", ephemeral=True)

    @commands.hybrid_command()
    @app_commands.describe(participant1="Participant that receives the first score")
    @app_commands.describe(score1="The first score")
    @app_commands.describe(participant2="Participant that receives the second score")
    @app_commands.describe(score2="The second score")
    async def result(self, ctx, participant1, score1:float, participant2, score2:float):
        """
        (League) Add a result to the competition.

        Command can only be used by the moderators and the host.
        Command usage: cb.result Participant1 Score1 Participant2 Score2
        """
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting result in {ctx.channel.id}: {participant1} {score1}:{score2} {participant2}")
            competition.result(self.convert_to_tag(ctx.author), participant1, score1, participant2, score2)
            self.logger.info(f"Setting result was succesful")
            await self.update_message(ctx.channel.id)
            await ctx.send(f"Result {participant1} {score1}:{score2} {participant2} set", ephemeral=True)
        except ParticipantDoesntExistException as e:
            await e.send_message(ctx)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    @app_commands.describe(participant="Participant who gets the score")
    @app_commands.describe(score="The score")
    async def score(self, ctx, participant, score: float):
        """
        (Generic) Set a score for a participant.

        Command can only be used by the moderators and the host.
        Command usage: cb.score Participant Score
        """
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting score in {ctx.channel.id}: {participant} {score}")
            competition.set_score(self.convert_to_tag(ctx.author), participant, score)
            self.logger.info(f"Setting score was succesful")
            await self.update_message(ctx.channel.id)
            await ctx.send(f"Score {score} set for {participant}", ephemeral=True)
        except UnsupportedCompetitionTypeException as e:
            await e.send_message(ctx)
        except NotAModException as e:
            await e.send_message(ctx)
        except ParticipantDoesntExistException as e:
            await e.send_message(ctx)     

    @commands.hybrid_command()
    @app_commands.describe(participant="Participant who the score is added to")
    @app_commands.describe(score="The score added")
    async def add_score(self, ctx, participant, score: float):
        """
        (Generic) Add score to a participant.

        Command can only be used by the moderators and the host.
        Command usage: cb.score Participant Score
        """
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Setting score in {ctx.channel.id}: {participant} {score}")
            competition.add_score(self.convert_to_tag(ctx.author), participant, score)
            self.logger.info(f"Setting score was succesful")
            await self.update_message(ctx.channel.id)
        except UnsupportedCompetitionTypeException as e:
            await e.send_message(ctx)
        except NotAModException as e:
            await e.send_message(ctx)
        except ParticipantDoesntExistException as e:
            await e.send_message(ctx)       

    @commands.hybrid_command()
    async def finish(self, ctx):
        """
        End the competition.

        Can only be used by the moderators and the host.
        """
        try:
            competition = self.competitions[ctx.channel.id]
            self.logger.info(f"Trying to finish {competition.thread.id}")
            competition.end(self.convert_to_tag(ctx.author))
            await self.update_message(ctx.channel.id, False)
            self.logger.info(f"Competition {competition.thread.id} has been finished.")
            await ctx.send("Competition is now finished", ephemeral=True)
            self.competitions[competition] = None
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.hybrid_command()
    @app_commands.describe(user="The user who will be added as the competitions moderator")
    async def add_mod(self, ctx, user):
        """
        Add a moderator to the competition.

        Command can only be used by the host.
        """
        try:
            competition = self.competitions[ctx.channel.id]
            competition.add_mod(f'<@{ctx.author.id}>', user)
            await ctx.channel.send(f"Added {user} as a mod", ephemeral=True)
            await self.update_message(ctx.channel.id)
        except NotAHostException as e:
            await e.send_message(ctx)


    # Helper functions
    def convert_to_tag(self, author):
        return f"<@{author.id}>"

    async def update_message(self, thread_id, active=True):
        competition = self.competitions[thread_id]
        message = competition.message
        table = competition.get_results()
        buttons = competition.buttons if active else None
        await self.edit_message(message, table, buttons)

    async def edit_message(self, message, message_text, view=None):
        try:
            await message.edit(content=message_text, view=view)
        except Exception as e:
            self.logger.error(e.with_traceback())

    async def add_participant_from_message(self, message_id, participant):
        competition = None
        for comp in self.competitions:
            comp = self.competitions[comp]
            if comp.message.id == message_id:
                competition = comp
        try:
            competition.add_participant(competition.host, participant)
            await self.update_message(message_id)
            await competition.thread.send(f"{participant} added to competition.")
        except ParticipantExistsException as e:
            await e.send_message(competition.thread)
        except NotAModException as e:
            await e.send_message(competition.thread)

    async def end_from_message(self, message_id, user):
        competition = None
        for comp in self.competitions:
            comp = self.competitions[comp]
            if comp.message.id == message_id:
                competition = comp
        try:
            competition.end(self.convert_to_tag(user))
            await self.update_message(competition.thread.id, False)
            self.logger.info(f"Competition {competition.thread.id} has been finished.")
        except NotAModException as e:
            await e.send_message(competition.thread)
        
async def setup(bot):
    await bot.add_cog(CompetitionHandler(bot))
