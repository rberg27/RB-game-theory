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
        "hou",
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
    def __init__(self, year: int, superbowl_winner: str, conference_champions: List[str],  firstround_losers: List[str], division_winners: List[str] = [], wildcard_winners: List[str] = []):
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
            scores[team] = round(self.records[team] * WIN, 1)
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
    #2024 season
    season_2024 = Season(2024, 'phi', ['phi', 'kc'], ['pit', 'den', 'la cha', 'tb', 'min', 'gb'], division_winners=['phi','buf', 'kc', 'was'], wildcard_winners=['hou', 'bal', 'buf', 'phi', 'was', 'la ram', 'kc', 'det'])
    season_2024.set_record('phi', 14)
    season_2024.set_record('was', 12)
    season_2024.set_record('dal', 7)
    season_2024.set_record('ny gia', 3)
    season_2024.set_record('tb', 10)
    season_2024.set_record('atl', 8)
    season_2024.set_record('car', 5)
    season_2024.set_record('no', 5)
    season_2024.set_record('la', 10)
    season_2024.set_record('sea', 10)
    season_2024.set_record('ari', 8)
    season_2024.set_record('sf', 6)
    season_2024.set_record('det', 15)
    season_2024.set_record('min', 14)
    season_2024.set_record('gb', 11)
    season_2024.set_record('chi', 5)
    season_2024.set_record('kc', 15)
    season_2024.set_record('la cha', 11)
    season_2024.set_record('den', 10)
    season_2024.set_record('lv', 4)
    season_2024.set_record('buf', 13)
    season_2024.set_record('mia', 8)
    season_2024.set_record('ny jet', 5)
    season_2024.set_record('ne', 4)
    season_2024.set_record('hou', 10)
    season_2024.set_record('ind', 8)
    season_2024.set_record('jac', 4)
    season_2024.set_record('ten', 3)
    season_2024.set_record('bal', 12)
    season_2024.set_record('cin', 9)
    season_2024.set_record('cle', 3)
    scores_2024 = season_2024.get_points()
    print(scores_2024)

    #2023 season
    season_2023 = Season(2023, 'kc', ['kc', 'sf'], ['cle', 'mia', 'pit', 'phi', 'la ram', 'gb'], division_winners=['kc', 'sf', 'bal', 'det'], wildcard_winners=['hou', 'kc', 'buf', 'tb', 'det', 'dal', 'bal', 'sf'])
    season_2023.set_record('phi', 11)
    season_2023.set_record('was', 4)
    season_2023.set_record('dal', 12)
    season_2023.set_record('ny gia', 6)
    season_2023.set_record('tb', 9)
    season_2023.set_record('atl', 7)
    season_2023.set_record('car', 2)
    season_2023.set_record('no', 9)
    season_2023.set_record('la ram', 10)
    season_2023.set_record('sea', 9)
    season_2023.set_record('ari', 4)
    season_2023.set_record('sf', 12)
    season_2023.set_record('det', 12)
    season_2023.set_record('min', 7)
    season_2023.set_record('gb', 9)
    season_2023.set_record('chi', 7)
    season_2023.set_record('kc', 11)
    season_2023.set_record('la cha', 5)
    season_2023.set_record('den', 8)
    season_2023.set_record('lv', 8)
    season_2023.set_record('buf', 11)
    season_2023.set_record('mia', 11)
    season_2023.set_record('ny jet', 7)
    season_2023.set_record('ne', 4)
    season_2023.set_record('hou', 10)
    season_2023.set_record('ind', 9)
    season_2023.set_record('jac', 9)
    season_2023.set_record('ten', 6)
    season_2023.set_record('bal', 13)
    season_2023.set_record('pit', 10)
    season_2023.set_record('cin', 9)
    season_2023.set_record('cle', 11)
    scores_2023 = season_2023.get_points()
    print(scores_2023)

    season_2022 = Season(2022, 'kc', ['kc', 'phi'], ['bal', 'mia', 'la cha', 'tb', 'sea', 'min'], division_winners=['phi', 'sf', 'kc', 'cin'], wildcard_winners=['cin', 'buf', 'jac', 'kc', 'dal', 'sf', 'ny gia', 'phi'])
    season_2022.set_record('kc', 14)
    scores_2022 = season_2022.get_points()
    print(scores_2022)
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
    season_1966.set_record('buf', 9)
    season_1966.set_record('bos', 8)
    season_1966.set_record('ny jet', 6)
    season_1966.set_record('hou', 3)
    season_1966.set_record('kc', 11)
    season_1966.set_record('sd', 7)
    season_1966.set_record('oak', 8)
    season_1966.set_record('den', 4)
    scores_1966 = season_1966.get_points()
    print(scores_1966)

if __name__ == "__main__":
    main()

