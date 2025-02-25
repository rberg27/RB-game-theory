from typing import List

abv = { "Arizona Cardinals": "car",
        "Atlanta Falcons": "fal",
        "Baltimore Colts": "col",
        "Baltimore Ravens": "rav",
        "Boston Patriots": "pat",
        "Buffalo Bills": "bil",
        "Carolina Panthers": "pan",
        "Chicago Bears":"bea",
        "Cincinnati Bengals":"ben",
        "Cleveland Browns":"brown",
        "Dallas Cowboys":"cow",
        "Denver Broncos":"bronc",
        "Detroit Lions":"lio",
        "Green Bay Packers":"pac",
        "Houston Oilers":"oil",
        "Houston Texans":"tex",
        "Indianapolis Colts":"col",
        "Jacksonville Jaguars":"jag",
        "Kansas City Chiefs":"chi",
        "Las Vegas Raiders":"rai",
        "Los Angeles Chargers": "cha",
        "Los Angeles Rams":"ram",
        "Miami Dolphins":"dol",
        "Minnesota Vikings":"vik",
        "New England Patriots": "pat",
        "New Orleans Saints": "sai",
        "New York Giants": 'gia',
        "New York Jets": 'jet',
        "Oakland Raiders": 'rai',
        "Philadelphia Eagles": 'eag',
        "Phoenix Cardinals": 'car',
        "Pittsburgh Steelers": 'ste',
        "San Diego Chargers": 'cha',
        "San Francisco 49ers": '49',
        "Seattle Seahawks": 'sea',
        "St. Louis Cardinals": 'car',
        "St. Louis Rams": 'ram',
        "Tampa Bay Buccaneers": 'buc',
        "Tennessee Titans": 'tit',
        "Washington Redskins": 'red',
        "Washington Football Team": 'foo',
        "Washington Commanders": 'com'
}

nfl_teams_2022_2024 = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]
nfl_teams_2020_2021 = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Football Team"
]

nfl_teams_2017_2019 = [
    "Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets",  # AFC East
    "Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers",  # AFC North
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans",  # AFC South
    "Denver Broncos", "Kansas City Chiefs", "Oakland Raiders", "San Diego Chargers",  # AFC West
    "Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Redskins",  # NFC East
    "Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings",  # NFC North
    "Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers",  # NFC South
    "Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"  # NFC West
]

nfl_teams_2016 = [
    "Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets",  # AFC East
    "Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers",  # AFC North
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans",  # AFC South
    "Denver Broncos", "Kansas City Chiefs", "Oakland Raiders", "San Diego Chargers",  # AFC West
    "Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Redskins",  # NFC East
    "Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings",  # NFC North
    "Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers",  # NFC South
    "Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"  # NFC West
]

nfl_teams_2002_2015 = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Miami Dolphins", "Minnesota Vikings", "New England Patriots", "New Orleans Saints",
    "New York Giants", "New York Jets", "Oakland Raiders", "Philadelphia Eagles",
    "Pittsburgh Steelers", "San Diego Chargers", "San Francisco 49ers", "Seattle Seahawks",
    "St. Louis Rams", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Redskins"
]

nfl_teams_1966 = [
    "Atlanta Falcons", "Baltimore Colts", "Chicago Bears", "Cleveland Browns",
    "Dallas Cowboys", "Detroit Lions", "Green Bay Packers", "Los Angeles Rams",
    "Minnesota Vikings", "New York Giants", "Philadelphia Eagles", "Pittsburgh Steelers",
    "St. Louis Cardinals", "San Francisco 49ers", "Washington Redskins",
    "Boston Patriots", "Buffalo Bills", "Denver Broncos", "Houston Oilers",
    "Kansas City Chiefs", "Miami Dolphins", "New York Jets", "Oakland Raiders",
    "San Diego Chargers"
]

SUPERBOWL_WIN = 5
CONFERENCE_WIN = 4
DIVISION_WIN = 3
WILDCARD_WIN = 2
FIRSTROUND_LOSS = 1
WIN = .2
class Season():
    def __init__(self, year: int, teams: List[str], superbowl_winner: str, conference_champions: List[str],  firstround_losers: List[str], division_winners: List[str] = [], wildcard_winners: List[str] = []):
        self.year = year
        self.teams = teams
        self.abv_to_team = {abv[team]:team for team in self.teams}
        self.superbowl_winner = self.abv_to_team[superbowl_winner]
        self.conference_champions = [self.abv_to_team[abv] for abv in conference_champions]
        self.division_winners =  [self.abv_to_team[abv] for abv in division_winners]
        self.wildcard_winners =  [self.abv_to_team[abv] for abv in wildcard_winners]
        self.firstround_losers =  [self.abv_to_team[abv] for abv in firstround_losers]
        self.scores = {team:0 for team in teams}

    def set_record(self, abv: str, wins: int):
        self.scores[self.abv_to_team[abv]] = wins
            
    def set_points(self):
        for team in self.teams:
            self.scores[team] = round(self.scores[team] * WIN, 1)
            if (team == self.superbowl_winner):
                self.scores[team] += SUPERBOWL_WIN
            if (team in self.conference_champions):
                self.scores[team] += CONFERENCE_WIN
            if (team in self.division_winners):
                self.scores[team] += DIVISION_WIN
            if (team in self.wildcard_winners):
                self.scores[team] += WILDCARD_WIN
            if (team in self.firstround_losers):
                self.scores[team] += FIRSTROUND_LOSS
                
    def get_points(self):
        return self.scores
    
    def verify_ian_didnt_typo(self):
        print(f'Verifying {self.year}')
        for team, value in self.scores.items():
            if (value == 0):
                print(f'{team} has 0 points')
        print() 

def main():
    #2024 season
    season_2024 = Season(2024, nfl_teams_2022_2024, 'eag', ['eag', 'chi'], ['ste', 'bronc', 'cha', 'buc', 'vik', 'pac'], division_winners=['eag','bil', 'chi', 'com'], wildcard_winners=['tex', 'rav', 'bil', 'eag', 'com', 'ram', 'chi', 'lio'])
    season_2024.set_record('eag', 14)
    season_2024.set_record('com', 12)
    season_2024.set_record('cow', 7)
    season_2024.set_record('gia', 3)
    season_2024.set_record('buc', 10)
    season_2024.set_record('fal', 8)
    season_2024.set_record('pan', 5)
    season_2024.set_record('sai', 5)
    season_2024.set_record('ram', 10)
    season_2024.set_record('sea', 10)
    season_2024.set_record('car', 8)
    season_2024.set_record('49', 6)
    season_2024.set_record('lio', 15)
    season_2024.set_record('vik', 14)
    season_2024.set_record('pac', 11)
    season_2024.set_record('bea', 5)
    season_2024.set_record('chi', 15)
    season_2024.set_record('cha', 11)
    season_2024.set_record('bronc', 10)
    season_2024.set_record('rai', 4)
    season_2024.set_record('bil', 13)
    season_2024.set_record('dol', 8)
    season_2024.set_record('jet', 5)
    season_2024.set_record('pat', 4)
    season_2024.set_record('tex', 10)
    season_2024.set_record('col', 8)
    season_2024.set_record('jag', 4)
    season_2024.set_record('tit', 3)
    season_2024.set_record('rav', 12)
    season_2024.set_record('ben', 9)
    season_2024.set_record('brown', 3)
    season_2024.set_record('ste', 10)
    season_2024.set_points()
    season_2024.verify_ian_didnt_typo()

    #2023 season
    season_2023 = Season(2023, nfl_teams_2022_2024, 'chi', ['chi', '49'], ['brown', 'dol', 'ste', 'eag', 'ram', 'pac'], division_winners=['chi', '49', 'rav', 'lio'], wildcard_winners=['tex', 'chi', 'bil', 'buc', 'lio', 'cow', 'rav', '49'])
    season_2023.set_record('eag', 11)
    season_2023.set_record('com', 4)
    season_2023.set_record('cow', 12)
    season_2023.set_record('gia', 6)
    season_2023.set_record('buc', 9)
    season_2023.set_record('fal', 7)
    season_2023.set_record('pan', 2)
    season_2023.set_record('sai', 9)
    season_2023.set_record('ram', 10)
    season_2023.set_record('sea', 9)
    season_2023.set_record('car', 4)
    season_2023.set_record('49', 12)
    season_2023.set_record('lio', 12)
    season_2023.set_record('vik', 7)
    season_2023.set_record('pac', 9)
    season_2023.set_record('bea', 7)
    season_2023.set_record('chi', 11)
    season_2023.set_record('cha', 5)
    season_2023.set_record('bronc', 8)
    season_2023.set_record('rai', 8)
    season_2023.set_record('bil', 11)
    season_2023.set_record('dol', 11)
    season_2023.set_record('jet', 7)
    season_2023.set_record('pat', 4)
    season_2023.set_record('tex', 10)
    season_2023.set_record('col', 9)
    season_2023.set_record('jag', 9)
    season_2023.set_record('tit', 6)
    season_2023.set_record('rav', 13)
    season_2023.set_record('ste', 10)
    season_2023.set_record('ben', 9)
    season_2023.set_record('brown', 11)
    season_2023.set_points()
    season_2023.verify_ian_didnt_typo()

    season_2022 = Season(2022, nfl_teams_2022_2024, 'chi', ['chi', 'eag'], ['rav', 'dol', 'cha', 'buc', 'sea', 'vik'], division_winners=['eag', '49', 'chi', 'ben'], wildcard_winners=['ben', 'bil', 'jag', 'chi', 'cow', '49', 'gia', 'eag'])
    season_2022.set_record('chi', 14)
    season_2022.set_record('eag', 14)
    season_2022.set_record('bil',13)
    season_2022.set_record('vik', 13)
    season_2022.set_record('49', 13)
    season_2022.set_record('ben', 12)
    season_2022.set_record('cow', 12)
    season_2022.set_record('rav', 10)
    season_2022.set_record('cha', 10)
    season_2022.set_record('gia', 9)
    season_2022.set_record('lio', 9)
    season_2022.set_record('jag', 9) #DOUGGIE PEDERSON
    season_2022.set_record('dol', 9)
    season_2022.set_record('ste', 9)
    season_2022.set_record('sea', 9)
    season_2022.set_record('com', 8)
    season_2022.set_record('pac', 8)
    season_2022.set_record('pat', 8)
    season_2022.set_record('buc', 8)
    season_2022.set_record('fal', 7)
    season_2022.set_record('pan', 7) #CMC dominance? this will be weird cuz he was the best rb but mid record
    season_2022.set_record('brown', 7) #same with chubb
    season_2022.set_record('sai', 7) #same with kamara
    season_2022.set_record('jet', 7)
    season_2022.set_record('tit', 7) #same with henry
    season_2022.set_record('rai', 6) #same with josh jacobs?
    season_2022.set_record('bronc', 5) #not the same with pookie (jabunzo williams)
    season_2022.set_record('ram', 5)
    season_2022.set_record('col', 4)
    season_2022.set_record('car', 4)
    season_2022.set_record('tex', 3)
    season_2022.set_record('bea', 3)  
    season_2022.set_points()
    season_2022.verify_ian_didnt_typo()

    #2021 season
    season_2021 = Season(2021, nfl_teams_2020_2021, 'ram', ['ram', 'ben'], ['cow', 'car', 'eag', 'rai', 'pat', 'ste'], division_winners=['ram', '49', 'ben', 'chi'], wildcard_winners=['49', 'pac', 'ram', 'buc', 'ben', 'tit', 'bil', 'chi'])
    season_2021.set_record('pac', 13)
    season_2021.set_record('buc', 13)
    season_2021.set_record('cow', 12) #first round exit
    season_2021.set_record('chi', 12)
    season_2021.set_record('ram', 12)
    season_2021.set_record('tit', 12)
    season_2021.set_record('car', 11)
    season_2021.set_record('bil', 11)
    season_2021.set_record('ben', 10)
    season_2021.set_record('rai', 10)
    season_2021.set_record('pat', 10)
    season_2021.set_record('49', 10)
    season_2021.set_record('ste', 9)
    season_2021.set_record('col', 9)
    season_2021.set_record('cha', 9)
    season_2021.set_record('dol', 9)
    season_2021.set_record('sai', 9)
    season_2021.set_record('eag', 9)
    season_2021.set_record('rav', 8)
    season_2021.set_record('brown', 8)
    season_2021.set_record('vik', 8)
    season_2021.set_record('fal', 7)
    season_2021.set_record('bronc', 7)
    season_2021.set_record('sea', 7)
    season_2021.set_record('foo', 7) #football team
    season_2021.set_record('bea', 6)
    season_2021.set_record('pan', 5)
    season_2021.set_record('tex', 4)
    season_2021.set_record('gia', 4)
    season_2021.set_record('jet', 4)
    season_2021.set_record('lio', 3)
    season_2021.set_record('jag', 3)
    season_2021.set_points()
    season_2021.verify_ian_didnt_typo()

    #2020 season
    season_2020 = Season(2020, nfl_teams_2020_2021, 'buc', ['chi', 'buc'], ['tit', 'col', 'ste', 'foo', 'bea', 'sea'], division_winners=['chi', 'bil', 'buc', 'pac'], wildcard_winners=['rav', 'bil', 'brown', 'chi', 'buc', 'sai', 'ram', 'pac'])
    season_2020.set_record('chi', 14)
    season_2020.set_record('bil',13)
    season_2020.set_record('pac', 13)
    season_2020.set_record('sai', 12)
    season_2020.set_record('ste', 12)
    season_2020.set_record('sea', 12)
    season_2020.set_record('rav', 11)
    season_2020.set_record('brown', 11)
    season_2020.set_record('col', 11)
    season_2020.set_record('buc', 11)
    season_2020.set_record('tit', 11)
    season_2020.set_record('ram', 10)
    season_2020.set_record('dol', 10)
    season_2020.set_record('car', 8)
    season_2020.set_record('bea', 8)
    season_2020.set_record('rai', 8)
    season_2020.set_record('cha', 7)
    season_2020.set_record('vik', 7)
    season_2020.set_record('pat', 7)
    season_2020.set_record('foo', 7)
    season_2020.set_record('cow', 6)
    season_2020.set_record('gia', 6)
    season_2020.set_record('49', 60)
    season_2020.set_record('pan', 5)
    season_2020.set_record('bronc', 5)
    season_2020.set_record('lio', 5)
    season_2020.set_record('ben', 4)
    season_2020.set_record('eag', 4)
    season_2020.set_record('fal', 4)
    season_2020.set_record('tex', 4)
    season_2020.set_record('jet', 2) #lmaoooo lost draft pick dumbass Adam Gase
    season_2020.set_record('jag', 1)
    season_2020.set_points()
    season_2020.verify_ian_didnt_typo()

    #2019 season
    season_2019 = Season(2019, nfl_teams_2017_2019, 'chi', ['chi', '49'], ['eag', 'sai', 'pat', 'bil'], division_winners=['chi','tit','pac','49'], wildcard_winners=['sea', 'pac', 'vik', '49', 'tit', 'rav', 'tex', 'chi'])
    season_2019.set_record('rav', 14)
    season_2019.set_record('pac', 13)
    season_2019.set_record('sai', 13)
    season_2019.set_record('49', 13)
    season_2019.set_record('chi', 13)
    season_2019.set_record('pat', 12)
    season_2019.set_record('sea', 11)
    season_2019.set_record('bil', 10)
    season_2019.set_record('tex', 10)
    season_2019.set_record('vik', 10)
    season_2019.set_record('ram', 9)
    season_2019.set_record('eag', 9)
    season_2019.set_record('tit', 9)
    season_2019.set_record('bea', 8)
    season_2019.set_record('cow', 8)
    season_2019.set_record('ste', 8)
    season_2019.set_record('fal', 7)
    season_2019.set_record('bronc', 7)
    season_2019.set_record('col', 7)
    season_2019.set_record('rai', 7)
    season_2019.set_record('jet', 7)
    season_2019.set_record('buc', 7)
    season_2019.set_record('brown', 6)
    season_2019.set_record('jag', 6)
    season_2019.set_record('car', 5)
    season_2019.set_record('pan', 5)
    season_2019.set_record('cha', 5)
    season_2019.set_record('dol', 5)
    season_2019.set_record('gia', 4)
    season_2019.set_record('lio', 3)
    season_2019.set_record('red', 3)
    season_2019.set_record('ben', 2)
    season_2019.set_points()
    season_2019.verify_ian_didnt_typo()


    #2018 season
    season_2018 = Season(2018, nfl_teams_2017_2019, "pat", ["pat", "ram"], ["rav", "tex", "sea", "bea"], division_winners=["pat", "chi", "ram", "sai"], wildcard_winners=["cha", "pat", "col", "chi", "cow", "ram", "eag", "sai"])
    season_2018.set_record('ram', 13)
    season_2018.set_record('sai', 13)
    season_2018.set_record('bea', 12) #??
    season_2018.set_record('chi', 12)
    season_2018.set_record('cha', 12)
    season_2018.set_record('tex', 11)
    season_2018.set_record('pat', 11)
    season_2018.set_record('rav', 10)
    season_2018.set_record('cow', 10)
    season_2018.set_record('col', 10)
    season_2018.set_record('sea', 10)
    season_2018.set_record('pit', 9)
    season_2018.set_record('eag', 9)
    season_2018.set_record('tit', 9)
    season_2018.set_record('vik', 8)
    season_2018.set_record('brown', 7)
    season_2018.set_record('fal', 7)
    season_2018.set_record('pan', 7)
    season_2018.set_record('dol', 7)
    season_2018.set_record('red', 7)
    season_2018.set_record('pac', 6)
    season_2018.set_record('bil', 6)
    season_2018.set_record('ben', 6)
    season_2018.set_record('bronc', 6)
    season_2018.set_record('lio', 6)
    season_2018.set_record('jag', 5)
    season_2018.set_record('gia', 5)
    season_2018.set_record('buc', 5)
    season_2018.set_record('rai', 4)
    season_2018.set_record('jet', 4)
    season_2018.set_record('49', 4)
    season_2018.set_record('car', 3)
    season_2018.set_points()
    season_2018.verify_ian_didnt_typo()

    #2017 season
    season_2017 = Season(1977, nfl_teams_2017_2019, 'eag', ['eag', 'pat'], ['pan', 'ram', 'bil', 'chi'], division_winners=['vik','eag','jag','pat'], wildcard_winners=['sai','vik','fal','eag','jag','ste','tit','pat'])
    season_2017.set_record('vik', 13)
    season_2017.set_record('pat', 13)
    season_2017.set_record('eag', 13)
    season_2017.set_record('ste', 13)
    season_2017.set_record('pan', 11)
    season_2017.set_record('ram', 11)
    season_2017.set_record('sai', 11)
    season_2017.set_record('fal', 10)
    season_2017.set_record('jag', 10)
    season_2017.set_record('chi', 10)
    season_2017.set_record('rav', 9)
    season_2017.set_record('bil', 9)
    season_2017.set_record('cow', 9)
    season_2017.set_record('lio', 9)
    season_2017.set_record('cha', 9)
    season_2017.set_record('sea', 9)
    season_2017.set_record('tit', 9)
    season_2017.set_record('car', 8)
    season_2017.set_record('ben', 7)
    season_2017.set_record('pac', 7)
    season_2017.set_record('red', 7)
    season_2017.set_record('rai', 6)
    season_2017.set_record('dol', 6)
    season_2017.set_record('49', 6)
    season_2017.set_record('bea', 5)
    season_2017.set_record('bronc', 5)
    season_2017.set_record('jet', 5)
    season_2017.set_record('buc', 5)
    season_2017.set_record('tex', 4)
    season_2017.set_record('col', 4)
    season_2017.set_record('gia', 3)
    season_2017.set_record('brown', 0) #LMAOOOOOOO
    season_2017.set_points()
    season_2017.verify_ian_didnt_typo()

    #2016 season
    season_2016 = Season(2016, nfl_teams_2016, 'pat', ['fal', 'pat'], ['dol', 'rai', 'gia', 'lio'], division_winners=['ste', 'pat', 'pac', 'fal'], wildcard_winners=['pit', 'chi', 'tex', 'pat', 'pac', 'cow', 'sea', 'fal'])
    season_2016.set_record('pat', 14)
    season_2016.set_record('cow', 13) #hahahahahah
    season_2016.set_record('chi', 12)
    season_2016.set_record('rai', 12)
    season_2016.set_record('fal', 11)
    season_2016.set_record('gia', 11)
    season_2016.set_record('ste', 11)
    season_2016.set_record('sea', 10)
    season_2016.set_record('pac', 10)
    season_2016.set_record('dol', 10)
    season_2016.set_record('bronc', 9)
    season_2016.set_record('lio', 9)
    season_2016.set_record('tex', 9)
    season_2016.set_record('buc', 9)
    season_2016.set_record('tit', 9)
    season_2016.set_record('red', 8)
    season_2016.set_record('rav', 8)
    season_2016.set_record('col', 8)
    season_2016.set_record('vik', 8)
    season_2016.set_record('car', 7)
    season_2016.set_record('bil', 7)
    season_2016.set_record('sai', 7)
    season_2016.set_record('eag', 7)
    season_2016.set_record('ben', 6)
    season_2016.set_record('pan', 6)
    season_2016.set_record('cha', 5)
    season_2016.set_record('jet', 5)
    season_2016.set_record('ram', 4)
    season_2016.set_record('bea', 3)
    season_2016.set_record('jag', 3)
    season_2016.set_record('49', 2)
    season_2016.set_record('brown', 1)
    season_2016.set_points()
    season_2016.verify_ian_didnt_typo()

    #2015 season
    season_2015 = Season(2015, nfl_teams_2002_2015, 'bronc', ['pan', 'bronc'], ['red', 'min', 'tex', 'ben'], division_winners=['car', 'pan', 'pat', 'bronc'], wildcard_winners=['pac', 'car', 'sea', 'pan', 'chi', 'pat', 'ste', 'bronc'])
    season_2015.set_record('pan', 15)
    season_2015.set_record('car', 13)
    season_2015.set_record('ben', 12)
    season_2015.set_record('bronc', 12)
    season_2015.set_record('pat', 12)
    season_2015.set_record('chi', 11)
    season_2015.set_record('vik', 11)
    season_2015.set_record('pac', 10)
    season_2015.set_record('jet', 10)
    season_2015.set_record('ste', 10)
    season_2015.set_record('sea', 10)
    season_2015.set_record('tex', 9)
    season_2015.set_record('red', 9)
    season_2015.set_record('fal', 8)
    season_2015.set_record('bil', 8)
    season_2015.set_record('lio', 7)
    season_2015.set_record('rai', 7)
    season_2015.set_record('ram', 7)
    season_2015.set_record('sai', 7)
    season_2015.set_record('eag', 7)
    season_2015.set_record('bea', 6)
    season_2015.set_record('dol', 6)
    season_2015.set_record('gia', 6)
    season_2015.set_record('buc', 6)
    season_2015.set_record('rav', 5)
    season_2015.set_record('jag', 5)
    season_2015.set_record('49', 5)
    season_2015.set_record('cow', 4)
    season_2015.set_record('cha', 4)
    season_2015.set_record('brown', 3)
    season_2015.set_record('tit', 3)
    season_2015.set_points()
    season_2015.verify_ian_didnt_typo()

    #2014 season
    season_2014 = Season(2014, nfl_teams_2002_2015, 'pat', ['sea', 'pat'], ['ben', 'ste', 'lio', 'car'], division_winners=['col', 'pat', 'pac', 'sea'], wildcard_winners=['col', 'den', 'rav', 'pat', 'cow', 'pac', 'pan', 'sea'])
    season_2014.set_record('cow', 12)
    season_2014.set_record('bronc', 12)
    season_2014.set_record('pac', 12)
    season_2014.set_record('pat', 12)
    season_2014.set_record('sea', 12)
    season_2014.set_record('car', 11)
    season_2014.set_record('lio', 11)
    season_2014.set_record('col', 11)
    season_2014.set_record('ste', 11)
    season_2014.set_record('ben', 10)
    season_2014.set_record('rav', 10)
    season_2014.set_record('eag', 10)
    season_2014.set_record('bil', 9)
    season_2014.set_record('tex', 9)
    season_2014.set_record('chi', 9)
    season_2014.set_record('cha', 9)
    season_2014.set_record('dol', 8)
    season_2014.set_record('49', 8)
    season_2014.set_record('pan', 7)
    season_2014.set_record('brown', 7)
    season_2014.set_record('vik', 7)
    season_2014.set_record('sai', 7)
    season_2014.set_record('fal', 6)
    season_2014.set_record('ram', 6)
    season_2014.set_record('gia', 6)
    season_2014.set_record('bea', 5)
    season_2014.set_record('jet', 4)
    season_2014.set_record('red', 4)
    season_2014.set_record('jag', 3)
    season_2014.set_record('rai', 3)
    season_2014.set_record('buc', 2)
    season_2014.set_record('tit', 2)
    season_2014.set_points()
    season_2014.verify_ian_didnt_typo()
    
    #1966 season
    season_1966 = Season(1966, nfl_teams_1966, 'pac', ['chi', 'pac'], ['cow', 'bil'])
    season_1966.set_record('pac', 12)
    season_1966.set_record('chi', 11)
    season_1966.set_record('cow', 10)
    season_1966.set_record('bil', 9)
    season_1966.set_record('brown', 9)
    season_1966.set_record('col', 9)
    season_1966.set_record('eag', 9)
    season_1966.set_record('car', 8)
    season_1966.set_record('rai', 8)
    season_1966.set_record('ram', 8)
    season_1966.set_record('pat', 8)
    season_1966.set_record('cha', 7)
    season_1966.set_record('red', 7)
    season_1966.set_record('jet', 6)
    season_1966.set_record('49', 6)
    season_1966.set_record('bea', 5)
    season_1966.set_record('ste',5)
    season_1966.set_record('bronc', 4)
    season_1966.set_record('lio', 4)
    season_1966.set_record('vik', 4)
    season_1966.set_record('fal', 3)
    season_1966.set_record('dol', 3)
    season_1966.set_record('oil', 3)
    season_1966.set_record('gia', 1)
    season_1966.set_points()
    season_1966.verify_ian_didnt_typo()

if __name__ == "__main__":
    main()

