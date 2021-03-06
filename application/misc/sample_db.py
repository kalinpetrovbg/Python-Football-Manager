"""Generate database with teams."""
from application import db
from application.models import Teams, Players


def create_sample():
    """Build sample database."""
    teams = [
        Teams(name="Manchester United", league="English Premier League", logo="man"),
        Teams(name="Arsenal", league="English Premier League", logo="ars"),
        Teams(name="FC Kalin", league="Hattrick"),
        Teams(name="Barcelona", league="Spain Primera Division", logo="bar"),
        Teams(name="Juventus", league="Italian Serie A", logo="juv"),
        Teams(name="Roma", league="Italian Serie A", logo="rom"),
        Teams(name="Real Madrid", league="Spain Primera Division", logo="rea"),
    ]

    """Generate the database with players."""

    """Manchester United players"""
    manchester = [
        Players(first_name="David", last_name="De Gea", team_id=1, position="GK", overall=31, attack=4, middle=3, defence=87),
        Players(first_name="Alex", last_name="Telles", team_id=1, position="DEF", overall=42, attack=14, middle=31, defence=81),
        Players(first_name="Harry", last_name="Maguire", team_id=1, position="DEF", overall=48, attack=27, middle=33, defence=83),
        Players(first_name="Raphaël", last_name="Varane", team_id=1, position="DEF", overall=49, attack=23, middle=37, defence=87),
        Players(first_name="Diogo", last_name="Dalot", team_id=1, position="DEF", overall=43, attack=21, middle=29, defence=78),
        Players(first_name="Scott", last_name="McTominay", team_id=1, position="MID", overall=44, attack=12, middle=82, defence=38),
        Players(first_name="Paul", last_name="Pogba", team_id=1, position="MID", overall=49, attack=33, middle=86, defence=27),
        Players(first_name="Bruno", last_name="Fernandes", team_id=1, position="MID", overall=48, attack=35, middle=87, defence=22),
        Players(first_name="Jadon", last_name="Sancho", team_id=1, position="ATT", overall=42, attack=85, middle=26, defence=15),
        Players(first_name="Marcus", last_name="Rashford", team_id=1, position="ATT", overall=40, attack=83, middle=24, defence=13),
        Players(first_name="Cristiano", last_name="Ronaldo", team_id=1, position="ATT", overall=50, attack=91, middle=36, defence=22),
        ]

    """Arsenal players"""
    arsenal = [
        Players(first_name="Aaron", last_name="Ramsdale", team_id=2, position="GK", overall=29, attack=2, middle=3, defence=81),
        Players(first_name="Kieran", last_name="Tierney", team_id=2, position="DEF", overall=41, attack=20, middle=22, defence=81),
        Players(first_name="Gabriel", last_name="Magalhães", team_id=2, position="DEF", overall=45, attack=22, middle=31, defence=81),
        Players(first_name="Benjamin", last_name="White", team_id=2, position="DEF", overall=43, attack=21, middle=29, defence=80),
        Players(first_name="T", last_name="Tomiyasu", team_id=2, position="DEF", overall=42, attack=23, middle=26, defence=78),
        Players(first_name="Gabriel", last_name="Silva", team_id=2, position="MID", overall=39, attack=20, middle=79, defence=18),
        Players(first_name="Granit", last_name="Xhaka", team_id=2, position="MID", overall=44, attack=19, middle=79, defence=33),
        Players(first_name="Thomas", last_name="Partey", team_id=2, position="MID", overall=48, attack=23, middle=84, defence=37),
        Players(first_name="Bukayo", last_name="Saka", team_id=2, position="MID", overall=43, attack=27, middle=83, defence=18),
        Players(first_name="Martin", last_name="Ødegaard", team_id=2, position="ATT", overall=41, attack=83, middle=24, defence=16),
        Players(first_name="Alexandre", last_name="Lacazette", team_id=2, position="ATT", overall=38, attack=82, middle=20, defence=11),
        ]

    players = manchester + arsenal

    for team in teams:
        db.session.add(team)

    for player in players:
        db.session.add(player)

    db.session.commit()

