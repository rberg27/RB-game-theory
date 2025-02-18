from typing import List

teams = ["arizona",
        "atlanta",
        "baltimore",
        "boston",
        "buffalo",
        "carolina",
        "chicago",
        "cincinnati",
        "cleveland",
        "dallas",
        "denver",
        "detroit",
        "green bay",
        "houston oilers",
        "houston texans",
        "indianapolis",
        "jacksonville",
        "kansas city",
        "las vegas",
        "la chargers",
        "la rams",
        "miami",
        "minnesota",
        "new england",
        "new orleans",
        "new york giants",
        "new york jets",
        "oakland",
        "philadelphia",
        "phoenix",
        "pittsburgh",
        "san diego",
        "san francisco",
        "seattle",
        "st. louis cardinals",
        "st. Louis rams",
        "tampa bay",
        "tennessee",
        "washington commanders",
        "washington redskins"
        ]
SUPERBOWL_WIN = 5
CONFERENCE_WIN = 4
DIVISION_WIN = 3
WILDCARD_WIN = 2
FIRSTROUND_LOSS = 1
WIN = .2
class Season():
    def __init__(self, year: int, superbowl_winner: str, conference_champions: List[str],  firstround_losers: List[str], division_winners: List[str] = None, wildcard_winners: List[str] = None):
        self.year = year
        self.superbowl_winner = superbowl_winner
        self.conference_champions = conference_champions
        self.division_winners = division_winners
        self.wildcard_winners = wildcard_winners
        self.firstround_losers = firstround_losers
        self.records = {team:0 for team in teams}

    def set_record(self, team, wins):
        self.records[team] = wins
            
    def get_points(self):
        scores = {team:0 for team in teams}
        for team in teams:
            scores[team] = records[team] * WIN
            if (team == self.superbowl_winner):
                scores[team] += SUPERBOWL_WIN
            if (team in self.conference_champions):
                scores[team] += CONFERENCE_WIN
            if (team in self.division_winners):
                scores[team] += DIVISION_WIN
            if (team in self.wildcard_winners):
                scores[team] += WILDCARD_WIN
            if (team in self.firstround_losers):
                scores[team] += FIRSTROUND_LOSS
        return scores



