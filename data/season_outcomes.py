from typing import List

teams = ["ari",
        "atl",
        "bal",
        "bos",
        "buf",
        "car",
        "chi",
        "cin",
        "cle",
        "dal",
        "den",
        "det",
        "gb",
        "hou oil",
        "hou tex",
        "ind",
        "jac",
        "kc",
        "lv",
        "la cha",
        "la ram",
        "mia",
        "min",
        "ne",
        "no",
        "ny gia",
        "ny jet",
        "oak",
        "phi",
        "pho",
        "pit",
        "sd",
        "sf",
        "sea",
        "sl car",
        "sl ram",
        "tb",
        "ten",
        "was"
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

    def set_record(self, team: str, wins: int):
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


def main():
    #1966 season
    season_1966 = Season(1966, 'gb', ['kc', 'gb'], ['dal', 'buf'])
    season_1966.set_record('dal', 10)
    season_1966.set_record('phi', 9)
    season_1966.set_record('was', 7)
    season_1966.set_record('pit',5)
    season_1966.set_record('ny gia', 1)
    season_1966.set_record('sl car', 8)
    season_1966.set_record('cle', 7)
    season_1966.set_record('atl', 3)
    season_1966.set_record('gb', 12)
    season_1966.set_record('bal', 9)
    season_1966.set_record('chi', 5)
    season_1966.set_record('det', 4)
    season_1966.set_record('la ram', 8)
    season_1966.set_record('sf', 6)
    season_1966.set_record('min', 4)

if __name__ == "__main__":
    main()

