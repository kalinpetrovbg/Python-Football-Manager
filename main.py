import random

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app import db
from db.names import spanish_l_names, spanish_f_names
from db.players import Players
from db.teams import Teams
from db.users import Users
from stadium.stadium import Stadium
from weather.weather import WEATHER_TYPES


teams = ["Juventus", "Arsenal", "Manchester", "Liverpool", "Bayern", "Milan", "Inter", "Barcelona", "Real Madrid",
         "Lecce", "Man City", "Newcastle", "Paris", "Monaco", "Schalke", "Verona", "Lecce", "Borusia",
         ]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/settings")
def settings():
    return "Settings Page"


@app.route("/create")
def create():
    return "Create a New Team"


@app.route("/cup.html")
def cup():
    return render_template("cup.html")


@app.route("/cup-champions.html")
def cup_champions():
    return render_template("cup-champions.html")


@app.route("/select-team.html")
def select_team():
    return render_template("select-team.html")


@app.route("/team/<team_id>.html")
def team(team_id):
    team = Teams.query.filter_by(id=team_id).first()
    players = Players.query.filter_by(team_id=team.id).all()
    return render_template("team.html", team=team, players=players)


@app.route("/existing.html")
def existing():
    all_teams = Teams.query.all()

    data = {}
    for team in all_teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("existing.html", data=data)


@app.route("/build-team.html", methods=['GET', 'POST'])
def build_team():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['league']:
            flash('Please enter all the fields.', 'error')
        else:
            team = Teams(name=request.form['name'], league=request.form['league'])
            db.session.add(team)
            db.session.commit()

            team_id = team.id
            return redirect(url_for('add_players', team_id=team_id))

    return render_template("build-team.html")


@app.route("/add-players/<team_id>.html", methods=['GET', 'POST'])
def add_players(team_id):
    if request.method == 'POST':
        team = Teams.query.filter_by(id=team_id).first()
        players = Players.query.filter_by(team_id=team.id).all()

        position = request.form['position']
        if not position:
            flash('Please enter all the fields.', 'error')
        else:
            if position == "GK":
                player = Players(first_name=random.choice(spanish_f_names),
                                 last_name=random.choice(spanish_l_names),
                                 position="GK",
                                 team_id=team_id,
                                 attack=random.randint(1, 5),
                                 middle=random.randint(1, 10),
                                 defence=random.randint(60, 85),
                                 )
            elif position == "DEF":
                player = Players(first_name=random.choice(spanish_f_names),
                                 last_name=random.choice(spanish_l_names),
                                 position="DEF",
                                 team_id=team_id,
                                 attack=random.randint(10, 30),
                                 middle=random.randint(20, 40),
                                 defence=random.randint(60, 85),
                                 )

            elif position == "MID":
                player = Players(first_name=random.choice(spanish_f_names),
                                 last_name=random.choice(spanish_l_names),
                                 position="MID",
                                 team_id=team_id,
                                 attack=random.randint(15, 35),
                                 middle=random.randint(60, 85),
                                 defence=random.randint(15, 35),
                                 )

            elif position == "ATT":
                player = Players(first_name=random.choice(spanish_f_names),
                                 last_name=random.choice(spanish_l_names),
                                 position="ATT",
                                 team_id=team_id,
                                 attack=random.randint(60, 85),
                                 middle=random.randint(20, 40),
                                 defence=random.randint(10, 30),
                                 )

            player.overall = round((player.attack + player.middle + player.defence) / 3)

            db.session.add(player)
            db.session.commit()

            total_attack = db.session.query(func.avg(Players.attack)).filter(Players.team_id == team_id).scalar()
            team.attack = round(total_attack)
            total_middle = db.session.query(func.avg(Players.middle)).filter(Players.team_id == team_id).scalar()
            team.middle = round(total_middle)
            total_defence = db.session.query(func.avg(Players.defence)).filter(Players.team_id == team_id).scalar()
            team.defence = round(total_defence)

            team_overall = round((team.attack + team.middle + team.defence) / 3)
            team.overall = team_overall

            db.session.merge(team)
            db.session.commit()

            flash('Your player has been created.')
            players.append(player)

            return render_template("/add-players.html", team_id=team_id, team=team, players=players)
    else:
        team = Teams.query.filter_by(id=team_id).first()
        players = Players.query.filter_by(team_id=team.id).all()

        return render_template("add-players.html", team_id=team_id, team=team, players=players)


@app.route("/choose-opponent.html")
def choose_opponent():
    return render_template("choose-opponent.html")


@app.route("/lineup.html")
def lineup():
    return render_template("lineup.html")


@app.route("/play.html")
def play():
    class Game:
        pass

        @staticmethod
        def start():
            content = "Game is starting..."
            return content

    class HomeTeam:
        def __init__(self, name, power):
            self.name = name
            self.power = power

        def __str__(self):
            return f"Home team {self.name} with power {self.power}."

    class AwayTeam:
        def __init__(self, name, power):
            self.name = name
            self.power = power

        def __str__(self):
            return f"Away team {self.name} with power {self.power}."

    home_team = HomeTeam(random.choice(teams), 23)
    away_team = AwayTeam(random.choice(teams), 12)

    score = {home_team.name: 0, away_team.name: 0}
    scorers = {}

    time = 0

    weather = random.choice(WEATHER_TYPES)

    stadium = Stadium()
    stadium.generate_stadium()

    visitors = stadium.generate_visitors(weather=weather)
    welcome = stadium.print_message(weather=weather)

    while time <= 90:

        minute = random.randint(1, 15)
        time += minute

        if time >= 90:
            break

        goal = random.randint(0, 1)
        if goal == 0:
            continue

        random_side = random.choice([home_team.name, away_team.name])

        scorers[time] = random_side

        score[random_side] += goal

    return render_template("play.html", content=Game.start(), home=home_team, away=away_team, score=score,
                           scorers=scorers, stadium=stadium, visitors=visitors, welcome=welcome, weather=weather)


@app.route("/quick-game.html")
def quick_game():
    return render_template("quick-game.html")


@app.route("/multiplayer.html")
def multiplayer():
    return render_template("multiplayer.html")


@app.route("/opp-england.html")
def opp_england():
    teams = Teams.query.filter_by(league="English Premier League").all()

    data = {}
    for team in teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("opp-england.html", data=data)


@app.route("/opp-spain.html")
def opp_spain():
    teams = Teams.query.filter_by(league="Spain Primera Division").all()

    data = {}
    for team in teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("opp-spain.html", data=data)


@app.route("/opp-italy.html")
def opp_italy():
    teams = Teams.query.filter_by(league="Italian Serie A").all()

    data = {}
    for team in teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("opp-italy.html", data=data)


@app.route("/opp-germany.html")
def opp_germany():
    teams = Teams.query.filter_by(league="German Bundesliga").all()

    data = {}
    for team in teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("opp-germany.html", data=data)


@app.route("/opp-france.html")
def opp_france():
    teams = Teams.query.filter_by(league="French Ligue 1").all()

    data = {}
    for team in teams:
        players = Players.query.filter_by(team_id=team.id).all()
        stats = {'name': team.name, 'logo': team.logo,
                 'league': team.league, 'id': team.id,
                 'ovr': team.overall, 'att': team.attack,
                 'mid': team.middle, 'def': team.defence,
                 'count': len(players),
                 }
        data[team] = stats
    return render_template("opp-france.html", data=data)


@app.route('/login.html', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")

            return render_template('login.html')

        return redirect("/")    # Todo

    elif request.method == "GET":
        return render_template("/login.html")


@app.route("/logout.html")
def logout():
    return render_template("logout.html")


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing = Users.query.filter_by(username=username).first()

        if existing:
            flash('There is already an user with this username.')
            return redirect("/signup.html")  # Todo - to check it

        user = Users(username=username, password=generate_password_hash(password, method="sha256"))

        db.session.add(user)
        db.session.commit()

        return render_template("index.html")
    else:
        return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
