import random

class AwayTeam:
    def __init__(self, name, *players):
        self.name = name
        self.players = list(players)
        self.midfield = 25   # later to be calculated


Liverpool = AwayTeam("Liverpool", "Kalin", "Ivan", "Georgi")
RealMadrid = AwayTeam("Real Madrid")
BayernMunich = AwayTeam("Bayern Munich")

AWAY_TEAMS = random.choice([Liverpool, RealMadrid, BayernMunich])
away_team = AWAY_TEAMS.name
