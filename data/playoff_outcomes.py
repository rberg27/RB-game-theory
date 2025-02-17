import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup as soup

urls = ['https://www.profootballhof.com/news/2005/01/news-playoff-results-1960s/',
        'https://www.profootballhof.com/news/2005/01/news-playoff-results-1970s/',
        'https://www.profootballhof.com/news/2005/01/news-playoff-results-1980s/',
        'https://www.profootballhof.com/news/2005/01/news-playoff-results-1990s/',
        'https://www.profootballhof.com/news/2005/01/news-playoff-results-2000s/',
        'https://www.profootballhof.com/news/2005/01/news-playoff-results-2010s/'
    ]

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

class Playoffs():
    def __init__(self, year):
        self.year = year
        self.url = urls[5]
        if (year < 1970):
            self.url = urls[0]
        elif (year < 1980):
            self.url = urls[1]
        elif (year < 1990):
            self.url = urls[2]
        elif (year < 2000):
            self.url = urls[3]
        elif (year < 2010):
            self.url = urls[4]
        self.superbowl_winner, self.conference_champions, self.division_winners, self.wildcard_winners, self.firstround_losers = None, None, None, None 

    def set_1966(self):
        self.superbowl_winner = 'green bay'
        self.conference_champions = ['green bay', 'kansas city']
        self.firstround_losers = ['dallas', 'buffalo']

    def get_points(self):
        scores = {team:0 for team in teams}
        for team in teams:
            if (team == self.superbowl_winner):
                scores[team] += 5
            if (team in self.conference_champions):
                scores[team] += 4
            if (team in self.division_winners):
                scores[team] += 3
            if (team in self.wildcard_winners):
                scores[team] += 2
            if (team in self.firstround_losers):
                scores[team] += 1
        return scores

