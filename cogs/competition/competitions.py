from helpers.errors import *
from cogs.competition.participant import Participant, ParticipantDoesntExistException, ParticipantExistsException
from cogs.competition.competition_types import CompetitionType


class Competition:
    def __init__(self, title, message, thread, buttons=None):
        self.active = True
        self.type = CompetitionType.GENERIC
        self.participants = []
        self.title = title
        self.winner = None
        self.host = None
        self.mods = []
        self.win = 3
        self.draw = 1
        self.defeat = 0
        self.best_of = 1
        self.message = message
        self.thread = thread
        self.buttons = buttons

    # Common
    def add_participant(self, author, participant):
        if self.is_mod(author):
            for e_participant in self.participants:
                if e_participant.name == participant:
                    raise ParticipantExistsException()
            participant_object = Participant(self, participant)
            self.participants.append(participant_object)
            for e_participant in self.participants:
                e_participant.add_opponent(participant_object)
                participant_object.add_opponent(e_participant)
        else:
            raise NotAModException()

    def end(self, user):
        if self.is_mod(user):
            self.active = False
            self.title += " (Finished)"
        else:
            raise NotAModException()

    def set_host(self, host):
        self.host = host

    def is_mod(self, author):
        return author in self.mods or author == self.host

    def add_mod(self, author, host):
        raise NotAHostException
    
    def get_header(self):
        lines = [f"# {self.title}", f"Hosted by: {self.host}"]
        if len(self.mods) > 0:
            lines.append(F"Moderated by: {', '.join(self.mods)}")
        lines.append(f"Type: {self.type.name.lower()}")
        if self.best_of > 1:
            lines.append(f"Extra rules: Best of {self.best_of}")
        return lines

    def get_results(self):
        lines = self.get_header()
        lines.append("**Leaderboard**")
        lines += [f"{participant.get_line(i)}" for i, participant in enumerate(sorted(self.participants, key=lambda x: [-x.get_points()]))]
        return "\n".join(lines)

    def __repr__(self):
        return f"Title: {self.title}, Participants: {self.participants}"
    
    def __str__(self):
        return f"Title: {self.title}, Participants: {self.participants}"

    # Type specifics

    def result(self, author, part1, score1:float, part2, score2: float):
        raise UnsupportedCompetitionTypeException       
        
    def set_score(self, author, part, score: float):
        raise UnsupportedCompetitionTypeException
        
    def add_score(self, author, part, score: float):
        raise UnsupportedCompetitionTypeException
    
    def set_win(self, author, points):
        raise UnsupportedCompetitionTypeException
        
    def set_draw(self, author, points):
        raise UnsupportedCompetitionTypeException
        
    def set_defeat(self, author, points):
        raise UnsupportedCompetitionTypeException

    def set_best_of(self, author, count: int):
        raise UnsupportedCompetitionTypeException

class Generic(Competition):
    def __init__(self, title, message, thread, buttons=None):
        super().__init__(title, message, thread, buttons)

    def set_score(self, author, part, score: float):
        if self.is_mod(author):
            participant1 = None
            for participant in self.participants:
                if participant.name == part:
                    participant1 = participant
            if participant1 is None:
                raise ParticipantDoesntExistException()
            participant1.set_score(score)
        else:
            raise NotAModException()
        
    def add_score(self, author, part, score: float):
        if self.is_mod(author):
            participant1 = None
            for participant in self.participants:
                if participant.name == part:
                    participant1 = participant
            if participant1 is None:
                raise ParticipantDoesntExistException()
            participant1.add_score(score)
        else:
            raise NotAModException()


class League(Competition):
    def __init__(self, title, message, thread, buttons=None):
        super().__init__(title, message, thread, buttons)
        self.type = CompetitionType.LEAGUE

    def get_results(self):
        lines = self.get_header()
        lines.append(f"Points system: Victory: {self.win}, Draw: {self.draw}, Defeat: {self.defeat}")
        lines.append("**Leaderboard**")
        lines += [f"{participant.get_line(i)} (Difference: {participant.get_diff(True)})" for i, participant in enumerate(sorted(self.participants, key=lambda x: [-x.get_points(), -x.get_diff()]))]
        lines.append("**Games:**")
        for participant in self.participants:
            lines += participant.get_games_table_lines()
        return "\n".join(lines)
    
    def result(self, author, part1, score1:int, part2 = None, score2:int=None):
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
        
    def set_win(self, author, points):
        if self.is_mod(author):
            self.win = points
        else:
            raise NotAModException()
        
    def set_draw(self, author, points):
        if self.is_mod(author):
            self.draw = points
        else:
            raise NotAModException()
        
    def set_defeat(self, author, points):
        if self.is_mod(author):
            self.defeat = points
        else:
            raise NotAModException()

    def set_best_of(self, author, count: int):
        if count < 1:
            raise InvalidValueException()
        if self.is_mod(author):
            self.best_of = count
        else:
            raise NotAModException()
        