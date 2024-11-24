class LeagueGame:
    def __init__(self, competition):
        self.competition = competition
        self.score = -1
        self.o_score = -1
        self.active = False

    def set_score(self, score, o_score):
        if score % 1 == 0:
            score = int(score)
        if o_score % 1 == 0:
            o_score == int(o_score)
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
        if not self.active:
            return 0
        if self.score > self.o_score:
            return self.competition.win
        if self.score < self.o_score:
            return self.competition.defeat
        return self.competition.draw
    
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
