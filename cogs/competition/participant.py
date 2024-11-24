from cogs.competition.competition_types import CompetitionType
from cogs.competition.game import LeagueGame


class Participant:
    def __init__(self, competition, name):
        self.competition = competition
        self.name = name
        self.games = {}
        self.score = 0

    def get_line(self, place=-1):
        text = "points"
        points = self.get_points()
        if points == 1:
            text = "point"
        if place == -1:
            return f"{self.name}: {points} {text}"
        elif place == 0:
            return f"🥇 {self.name}: {points} {text}"
        elif place == 1:
            return f"🥈 {self.name}: {points} {text}"
        elif place == 2:
            return f"🥉 {self.name}: {points} {text}"
        return f"{place+1}. {self.name}: {points} {text}"
    
    def add_opponent(self, opponent):
        if self.competition.type == CompetitionType.LEAGUE:
            if opponent.name != self.name and opponent.name not in self.games:
                self.games[opponent.name] = LeagueGame(self.competition)

    def get_points(self):
        score = self.score
        if self.competition.type == CompetitionType.LEAGUE:
            score = 0
            for game in self.games:
                score += self.games[game].get_points()
        if score % 1 == 0:
            score = int(score)
        return score
        
    def get_diff(self, as_str=False):
        if self.competition.type == CompetitionType.LEAGUE:
            diff = 0
            plus = ""
            for game in self.games:
                diff += self.games[game].get_diff()
            if as_str:
                if diff > 0:
                    plus = "+"
                return f"{plus}{diff}"
            return diff
        return 0

    def set_score(self, score: float):
        self.score = score
    
    def add_score(self, score: float):
        self.score += score

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

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name


# Exceptions

class ParticipantExistsException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("Participant is already taking part.")


class ParticipantDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    async def send_message(self, ctx):
        await ctx.send("One of the participants doesn't take part.")
