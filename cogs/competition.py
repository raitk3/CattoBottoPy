"""Experimental things"""

from discord import Embed, ButtonStyle, Interaction, ChannelType, utils
from discord.ext import commands
import asyncio
import logging
from discord.ui import Button, View, button
from helpers.errors import *
from helpers.emoji import Emoji


class Game:
    def __init__(self):
        self.score = -1
        self.o_score = -1
        self.active = False

    def set_score(self, score, o_score):
        self.score = score
        self.o_score = o_score
        self.active = True

    def reset_score(self):
        self.active = False

    def get_diff(self):
        if not self.active:
            return 0
        return int(self.score) - int(self.o_score)

    def get_points(self):
        if self.active and self.score > self.o_score:
            return 1
        return 0
    
    def get_win_draw_loss(self):
        if self.score > self.o_score:
            return "victory"
        elif self.score < self.o_score:
            return "defeat"
        return "draw"
    
    def get_line(self):
        if self.active:
            return f"`{self.score}:{self.o_score} {self.get_win_draw_loss()}`"
        return ""


class Participant:
    def __init__(self, name):
        self.name = name
        self.games = {}

    def get_line(self, place=-1):
        text = "points"
        if self.get_points() == 1:
            text = "point"
        if place == -1:
            return f"{self.name}: {self.get_points()} {text}"
        elif place == 0:
            return f"🥇 {self.name}: {self.get_points()} {text}"
        elif place == 1:
            return f"🥈 {self.name}: {self.get_points()} {text}"
        elif place == 2:
            return f"🥉 {self.name}: {self.get_points()} {text}"
        return f"{place+1}. {self.name}: {self.get_points()} {text}"
    
    def add_opponent(self, opponent):
        if opponent.name != self.name and opponent.name not in self.games:
            self.games[opponent.name] = Game()

    def get_points(self):
        score = 0
        for game in self.games:
            score += self.games[game].get_points()
        return score
    
    def get_diff(self, as_str=False):
        diff = 0
        plus = ""
        for game in self.games:
            diff += self.games[game].get_diff()
        if as_str:
            if diff > 0:
                plus = "+"
            return f"{plus}{diff}"
        return diff

    def result(self, score, o, o_score):
        self.games[o].set_score(score, o_score)

    def get_games_table_lines(self):
        lines = [f"**{self.name}**:"]
        if len(self.games) == 0:
            lines.append("No games")
        for i, game in enumerate(self.games):
            if i+1 == len(self.games):
                lines.append(f"└ vs {game} {self.games[game].get_line()}")
            else:
                lines.append(f"├ vs {game} {self.games[game].get_line()}")
        return lines

    def __str__(self):
        return self.name


class Competition:
    def __init__(self, title, message, thread, buttons=None):
        self.active = True
        self.participants = []
        self.title = title
        self.winner = None
        self.host = None
        self.mods = []
        self.message = message
        self.thread = thread
        self.buttons = buttons

    def add_participant(self, author, participant):
        if self.is_mod(author):
            for e_participant in self.participants:
                if e_participant.name == participant:
                    raise ParticipantExistsException()
            participant_object = Participant(participant)
            self.participants.append(participant_object)
            for e_participant in self.participants:
                e_participant.add_opponent(participant_object)
                participant_object.add_opponent(e_participant)
        else:
            raise NotAModException()

    def end_competition(self, user):
        print(user)
        if self.is_mod(user):
            self.active = False
            self.title += " (Finished)"
        else:
            raise NotAModException()

    def result(self, author, part1, score1:int, part2, score2:int):
        if self.is_mod(author):
            participant1, participant2 = None, None
            for participant in self.participants:
                if participant.name == part1:
                    participant1 = participant
                elif participant.name == part2:
                    participant2 = participant
            if participant1 is None or participant2 is None:
                raise ParticipantDoesntExistException()
            participant1.result(score1, part2, score2)
            participant2.result(score2, part1, score1)
        else:
            raise NotAModException()

    def set_host(self, host):
        self.host = host
    
    def add_mod(self, author, host):
        if author == self.host:
            self.mods.append(host)
        else:
            raise NotAHostException()

    def is_mod(self, author):
        return author in self.mods or author == self.host
    
    def get_table(self):
        lines = [f"# {self.title}", f"Hosted by: {self.host}"]
        if len(self.mods) > 0:
            lines.append(F"Moderated by: {', '.join(self.mods)}")
        lines.append("**Leaderboard**")
        lines += [f"{participant.get_line(i)} (Difference: {participant.get_diff(True)})" for i, participant in enumerate(sorted(self.participants, key=lambda x: [-x.get_points(), -x.get_diff()]))]
        lines.append("**Games:**")
        for participant in self.participants:
            lines += participant.get_games_table_lines()
        return "\n".join(lines)

    def __str__(self):
        return f"Title: {self.title}, Participants: {self.participants}"


class CompetitionHandler(commands.Cog, name='Competition'):
    """Competition-leaderboard thing"""
    
    def __init__(self, bot):
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
            self.logger.info(f"{interaction.user} requested to be in the {interaction.message.id} competition")

            try:
                await self.competition_handler.add_participant_from_message(interaction.message.id, author)
            except Exception:
                pass
            await interaction.response.defer()

        @button(label="Finish", style=ButtonStyle.gray, emoji="🏁")
        async def end_competition(self, interaction: Interaction, button: Button):
            self.logger.info(f"{interaction.user} requested end the competition")
            try:
                await self.competition_handler.end_competition_from_message(interaction.message.id, interaction.user)
            except Exception:
                pass
            await interaction.response.defer()


    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Competition tools are loaded')

    @commands.command()
    async def competition(self, ctx, title="Competition"):
        competition_message = await ctx.send(f"{self.emoji.emoji.get('cat_loading', '')}Initialising competition")
        competition_thread = await competition_message.create_thread(name=title)
        competition = Competition(title, competition_message, competition_thread, buttons=self.Buttons(self))
        competition.set_host(self.convert_to_tag(ctx.author))
        self.competitions[competition_thread.id] = competition
        await self.update_message(competition.thread.id)
        await competition_thread.send("Competition initalisation  was successful")
        await ctx.message.delete()

    @commands.command()
    async def participant(self, ctx, participant=None):
        self.logger.info(f"Trying to add a participant to a competition")
        try:
            if participant is None:
                participant = ctx.author
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

    @commands.command()
    async def result(self, ctx, part1, score1, part2, score2):
        try:
            competition = self.competitions[ctx.channel.id]
            competition.result(self.convert_to_tag(ctx.author), part1, score1, part2, score2)
            await self.update_message(ctx.channel.id)
        except ParticipantDoesntExistException as e:
            await e.send_message(ctx)
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.command()
    async def finish(self, ctx):
        try:
            competition = self.competitions[ctx.channel.id]
            competition.end_competition(self.convert_to_tag(ctx.author))
            await self.update_message(ctx.channel.id, False)
            self.logger.info(f"Competition {competition.thread.id} has been finished.")
            self.competitions[competition] = None
        except NotAModException as e:
            await e.send_message(ctx)

    @commands.command()
    async def add_mod(self, ctx, user):
        try:
            competition = self.competitions[ctx.channel.id]
            competition.add_mod(f'<@{ctx.author.id}>', user)
            await ctx.channel.send(f"Added {user} as a mod")
            await self.update_message(ctx.channel.id)
        except NotAHostException as e:
            await e.send_message(ctx)


    # Helper functions
    def convert_to_tag(self, author):
        return f"<@{author.id}>"

    async def update_message(self, thread_id, active=True):
        competition = self.competitions[thread_id]
        message = competition.message
        table = competition.get_table()
        buttons = competition.buttons if active else None
        await self.edit_message(message, table, buttons)

    async def edit_message(self, message, message_text, view=None):
        await message.edit(content=message_text, view=view)

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

    async def end_competition_from_message(self, message_id, user):
        competition = None
        for comp in self.competitions:
            comp = self.competitions[comp]
            if comp.message.id == message_id:
                competition = comp
        try:
            competition.end_competition(self.convert_to_tag(user))
            await self.update_message(competition.thread.id, False)
            self.logger.info(f"Competition {competition.thread.id} has been finished.")
        except NotAModException as e:
            await e.send_message(competition.thread)
        
async def setup(bot):
    await bot.add_cog(CompetitionHandler(bot))
